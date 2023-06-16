// Package rules defines validation method for each rule set in rule.proto.
package rules

import (
	"fmt"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"

	"github.com/google/smbios-validation-tool/dmiparser"
	pb "github.com/google/smbios-validation-tool/rules/proto"

	"google.golang.org/protobuf/encoding/prototext"
)

// RuleUnmarshal parses the rule textproto into rule.proto format.
func RuleUnmarshal(path string) ([]*pb.TypeRule, error) {
	rulePb := &pb.RuleSet{}
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}
	if err := prototext.Unmarshal(data, rulePb); err != nil {
		return nil, err
	}
	return rulePb.GetTypeRule(), nil
}

// CountRequiredTables verifies the number of tables in each type
func CountRequiredTables(ruleList []*pb.TypeRule, records map[string]dmiparser.Record) bool {
	ruleCount := make(map[string]int)
	for _, rule := range ruleList {
		ruleCount[strconv.Itoa(int(rule.GetType()))] = int(rule.GetCount())
	}
	recordCount := make(map[string]int)
	for _, record := range records {
		recordCount[record.Type]++
	}

	for typeID, count := range ruleCount {
		if count > recordCount[typeID] {
			fmt.Printf("Not enough table type %v. Required: %d, Got %d\n", typeID, count, recordCount[typeID])
			return false
		}
	}
	return true
}

type fieldRule struct {
	field       string
	validations *pb.Validations
	errMsg      []string
}

type fieldRules []fieldRule

func newRules(r []*pb.Rule) fieldRules {
	var length int
	// Each GetField() may contains multiple fields.
	for _, rule := range r {
		length += len(rule.GetField())
	}
	rules := make([]fieldRule, length)
	i := 0
	for _, rule := range r {
		for _, field := range rule.GetField() {
			rules[i] = fieldRule{
				field:       field,
				validations: rule.GetValidations(),
				errMsg:      []string{},
			}
			i++
		}
	}
	return rules
}

type conditionalRule struct {
	condition fieldRules
	rules     fieldRules
}

// TypeRule defines the struct of *pb.TypeRule.
type TypeRule struct {
	tableType        int
	count            int
	rules            fieldRules
	conditionalRules []conditionalRule
}

// GetTypeRule returns the TypeRule for a single type of table.
func GetTypeRule(typeID string, rules []*pb.TypeRule) TypeRule {
	for _, rule := range rules {
		if typeID == strconv.Itoa(int(rule.GetType())) {
			condRules := make([]conditionalRule, len(rule.GetConditionalRule()))
			for i, rule := range rule.GetConditionalRule() {
				condRules[i] = conditionalRule{
					condition: newRules(rule.GetCondition()),
					rules:     newRules(rule.GetRule()),
				}
			}
			return TypeRule{
				tableType:        int(rule.GetType()),
				count:            int(rule.GetCount()),
				rules:            newRules(rule.GetRule()),
				conditionalRules: condRules,
			}
		}
	}
	return TypeRule{}
}

// NotEmpty returns true when TypeRule for specific typeID is found.
func (TR TypeRule) NotEmpty() bool {
	if len(TR.rules) == 0 && len(TR.conditionalRules) == 0 {
		return false
	}
	return true
}

// ValidateAll checks all rules within one type including conditional rules.
func (TR TypeRule) ValidateAll(handleID string, records map[string]dmiparser.Record) bool {
	compliance := TR.rules.validateAll(handleID, records)
	errMsg := TR.rules.collectErrMsg()
	if len(TR.conditionalRules) > 0 {
		for _, cond := range TR.conditionalRules {
			if cond.condition.validateAll(handleID, records) {
				compliance = cond.rules.validateAll(handleID, records) && compliance
				errMsg = append(errMsg, cond.rules.collectErrMsg()...)
			}
		}
	}
	if len(errMsg) > 0 {
		fmt.Printf("\033[4mHandle ID: %v, Type %v\033[0m\n", handleID, records[handleID].Type)
		for _, msg := range errMsg {
			fmt.Printf("%v", msg)
		}
		fmt.Println()
	}
	return compliance
}

// ValidateAll runs all the checks for all rules for a single type of table.
func (rules fieldRules) validateAll(handleID string, records map[string]dmiparser.Record) bool {
	compliance := true
	for i := range rules {
		compliance = rules[i].validateAll(handleID, records) && compliance
	}
	return compliance
}

func (rules fieldRules) collectErrMsg() []string {
	errMsg := []string{}
	for _, fieldRule := range rules {
		errMsg = append(errMsg, fieldRule.errMsg...)
	}
	return errMsg
}

// validateAll runs all the checks for a single field.
func (r *fieldRule) validateAll(handleID string, records map[string]dmiparser.Record) bool {
	record := records[handleID]
	// Presence must be checked before running other validators.
	if !r.validatePresence(record) {
		return false
	}
	compliance := true
	if r.validations.GetRegexpValidate() != nil {
		compliance = r.validateRegexp(record, r.validations.GetRegexpValidate()) && compliance
	}
	if r.validations.GetInListValidate() != nil {
		compliance = r.validateInList(record, r.validations.GetInListValidate()) && compliance
	}
	if r.validations.GetNotContainValidate() != nil {
		compliance = r.validateNotContain(record, r.validations.GetNotContainValidate()) && compliance
	}
	if r.validations.GetItemCountUniqueValidate() != -1 {
		compliance = r.validateItemUniqueCount(record, int(r.validations.GetItemCountUniqueValidate())) && compliance
	}
	if r.validations.GetHandleTypeValidate() != -1 {
		compliance = r.validateHandleType(record, records, int(r.validations.GetHandleTypeValidate())) && compliance
	}
	if r.validations.GetHandlesPresenceValidate() {
		compliance = r.validateHandlePresence(record, records) && compliance
	}
	return compliance
}

func (r *fieldRule) validatePresence(record dmiparser.Record) bool {
	if _, ok := record.Props[r.field]; !ok {
		r.addError("", fmt.Sprintf("Error: Field not found in table"))
		return false
	}
	if prop := record.Props[r.field]; prop.Val == "<BAD INDEX>" && prop.Item == nil {
		r.addError("", fmt.Sprintf("Error: Field is found but value and item are missing"))
		return false
	}
	return true
}

func (r *fieldRule) validateRegexp(record dmiparser.Record, re []byte) bool {
	prop := record.Props[r.field]
	pattern := regexp.MustCompile(string(re))
	if !pattern.MatchString(prop.Val) {
		r.addError(prop.Val, fmt.Sprintf("Error: %v doesn't match regex %v", prop.Val, string(re)))
	}
	return pattern.MatchString(prop.Val)
}

func (r *fieldRule) validateNotContain(record dmiparser.Record, list []string) bool {
	prop := record.Props[r.field]
	for _, val := range list {
		pattern := regexp.MustCompile(".*(" + val + ").*")
		if pattern.MatchString(prop.Val) {
			r.addError(prop.Val, fmt.Sprintf("Error: %v contains %v", prop.Val, list))
			return false
		}
	}
	return true
}

func (r *fieldRule) validateInList(record dmiparser.Record, list []string) bool {
	prop := record.Props[r.field]
	for _, val := range list {
		if prop.Val == val {
			return true
		}
	}
	r.addError(prop.Val, fmt.Sprintf("Error: %v is not in %v", prop.Val, list))
	return false
}

func (r *fieldRule) validateItemUniqueCount(record dmiparser.Record, itemLen int) bool {
	prop := record.Props[r.field]
	count, err := strconv.Atoi(prop.Val)
	if err != nil {
		r.addError(prop.Val, fmt.Sprintf("Error: %v is not a number", prop.Val))
		return false
	}
	if count*itemLen != len(prop.Item) {
		r.addError(prop.Val, fmt.Sprintf("Error: item count %v doesn't match number of items %v", count, len(prop.Item)/itemLen))
		return false
	}
	itemList := []string{}
	for i := 0; i < len(prop.Item); i += itemLen {
		itemList = append(itemList, strings.Join(prop.Item[i:i+itemLen], ""))
	}
	uniqueMap := make(map[string]bool)
	for _, item := range itemList {
		if uniqueMap[item] {
			r.addError("", fmt.Sprintf("Error: %v is duplicated", item))
		}
		uniqueMap[item] = true
	}
	if len(uniqueMap) != len(itemList) {
		return false
	}
	return true
}

func (r *fieldRule) validateHandleType(record dmiparser.Record, records map[string]dmiparser.Record, handleType int) bool {
	prop := record.Props[r.field]
	if prop.Val == "Not Provided" {
		return true
	}
	targetRecord, ok := records[prop.Val]
	if !ok {
		r.addError(prop.Val, fmt.Sprintf("Error: %v not found in smbios table", prop.Val))
		return false
	}
	if targetRecord.Type != strconv.Itoa(handleType) {
		r.addError(prop.Val, fmt.Sprintf("Error: %v(Type %v) is not type %v", prop.Val, records[prop.Val].Type, handleType))
		return false
	}
	return true
}

func (r *fieldRule) validateHandlePresence(record dmiparser.Record, records map[string]dmiparser.Record) bool {
	prop := record.Props[r.field]
	for _, item := range prop.Item {
		// Clean up possible string following the handle.
		handle, _, _ := strings.Cut(item, " ")
		pattern := regexp.MustCompile(string(`0[xX][0-9a-fA-F]{4}`))
		if !pattern.MatchString(handle) {
			r.addError(prop.Val, fmt.Sprintf("Error: %v doesn't match handle pattern %v", handle, "0[xX][0-9a-fA-F]{4}"))
		} else {
			_, ok := records[handle]
			if !ok {
				r.addError(prop.Val, fmt.Sprintf("Error: %v not found in smbios table", handle))
				return false
			}
		}
	}
	return true
}

func (r *fieldRule) addError(val, msg string) {
	r.errMsg = append(r.errMsg, fmt.Sprintf("Field: %v, Value: %v\n\033[31m%v\033[0m\n", r.field, val, msg))
}
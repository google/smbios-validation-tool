package main

import (
	"fmt"

	"flag"

	"github.com/google/smbios-validation-tool/dmiparser"
	"github.com/google/smbios-validation-tool/rules"
	pb "github.com/google/smbios-validation-tool/rules/proto"
)

var dmiFile *string = flag.String("table", "", "the path of the dmidecode dump")
var ruleFile *string = flag.String("rule", "", "the path of the rule.textproto")

func main() {

	flag.Parse()

	handleIDs, records, err := dmiparser.Parse(*dmiFile)
	if err != nil {
		fmt.Printf("Dmiparser Fail: %v\n", err)
		return
	}
	ruleList, err := rules.RuleUnmarshal(*ruleFile)
	if err != nil {
		fmt.Printf("RuleUnmarshal Fail: %v\n", err)
		return
	}
	compliance := validation(handleIDs, records, ruleList)
	fmt.Println("Rule:", *ruleFile)
	fmt.Println("Compliance:", compliance)
}

func validation(handleIDs []string, records map[string]dmiparser.Record, ruleList []*pb.TypeRule) bool {
	compliance := true
	// Check compliance for each fields.
	for _, handleID := range handleIDs {
		typeID := records[handleID].Type
		if typeRule := rules.GetTypeRule(typeID, ruleList); typeRule.NotEmpty() {
			compliance = typeRule.ValidateAll(handleID, records) && compliance
		}
	}
	// Check existence of required tables.
	compliance = rules.CountRequiredTables(ruleList, records) && compliance
	return compliance
}

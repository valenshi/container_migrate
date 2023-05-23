package main

import (
	"bytes"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
)

type HostInfo struct {
	host_name   string
	power       float64
	cpu_load    float64
	memory_load float64
	energy_cost float64
	power_limit float64
}

func toFloat(num string) float64 {
	res, err := strconv.ParseFloat(strings.TrimSpace(num), 64)
	if err != nil {
		return 0
	}
	return res
}

func initHostInfo(host_name string) (*HostInfo, error) {
	hostinfo := HostInfo{host_name, 0, 0, 0, 0, 0}
	ret, err := apiMethod(host_name, "hostPower")
	if err != nil {
		return nil, nil
	}
	hostinfo.power = toFloat(ret)

	ret, err = apiMethod(host_name, "powerLimit")
	if err != nil {
		return nil, nil
	}

	hostinfo.power_limit = toFloat(ret)

	ret, err = apiMethod(host_name, "energyCost")
	if err != nil {
		return nil, nil
	}

	hostinfo.energy_cost = toFloat(ret)

	return &hostinfo, nil
}

func main() {
	hostinfo, err := initHostInfo("node2")

	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(hostinfo)
}

func apiMethod(hostname string, method string) (string, error) {
	ip := "192.168.1.201"
	url := "http://" + ip + ":9926"

	payload := newAPIRequest(hostname, method)
	payloadXML, _ := xml.Marshal(payload)

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(payloadXML))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/xml")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", nil
	}

	respBody, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		// fmt.Println(err)
		return "", err
	}

	response := newAPIResponse()
	err = xml.Unmarshal(respBody, response)
	if err != nil {
		// fmt.Println(err)
		return "nil", err
	}
	return response.Result, err
}

func newAPIRequest(hostname string, method string) *APIRequest {
	return &APIRequest{
		Method: method,
		Params: []interface{}{hostname},
	}
}

type APIRequest struct {
	XMLName xml.Name      `xml:"methodCall"`
	Method  string        `xml:"methodName"`
	Params  []interface{} `xml:"params>param>value"`
}

type APIResponse struct {
	XMLName xml.Name `xml:"methodResponse"`
	Result  string   `xml:"params>param>value>string"`
}

func newAPIResponse() *APIResponse {
	return &APIResponse{}
}

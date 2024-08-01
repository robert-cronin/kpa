// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

package kubectl

import (
	"bytes"
	"fmt"
	"os/exec"
	"strings"
)

type Executor struct{}

func NewExecutor() *Executor {
	return &Executor{}
}

func (e *Executor) Execute(command string) (string, error) {
	args := strings.Fields(command)
	if len(args) == 0 || args[0] != "kubectl" {
		return "", fmt.Errorf("invalid kubectl command: %s", command)
	}

	cmd := exec.Command(args[0], args[1:]...)
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr

	err := cmd.Run()
	if err != nil {
		return "", fmt.Errorf("command failed: %v\nStderr: %s", err, stderr.String())
	}

	return out.String(), nil
}

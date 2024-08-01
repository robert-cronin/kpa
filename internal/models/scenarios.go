// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

package models

type Scenario struct {
	ID          int64    `json:"id"`
	Name        string   `json:"name"`
	Description string   `json:"description"`
	Tasks       []string `json:"tasks"`
	Validation  string   `json:"validation"`
}

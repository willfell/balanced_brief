################################################################################
# Variables
################################################################################
// Locals
locals {
  name = var.service
  slack_integration = {
    SLACK_CHANNEL    = "#brief-deploys"
    SLACK_CHANNEL_ID = "C068YND5RJB"
    SLACK_API_TOKEN  = data.aws_secretsmanager_secret_version.slack_token.secret_string
  }

}

// Variables
variable "cidr_private" {
  type        = string
  description = "The CIDR block of the private network."
  default     = "10.0.0.0/8"

  validation {
    condition     = can(regex("\\b[1][0]{1,2}(\\.([0-9]|[0-9]{2}|[01][0]{1,2}|2[0-4][0-9]|25[0-5])){3}(\\/([0-9]|[12][0-9]|3[0-2])){0,1}\\b", var.cidr_private))
    error_message = "The CIDR block must represent a IPv4 range between 10.0.0.0 and 10.255.255.255."
  }
}

variable "cidr_public" {
  type        = string
  description = "The CIDR block to allow all traffic."
  default     = "0.0.0.0/0"

  validation {
    condition     = can(regex("^([0][.][0][.][0][.][0][/][0])$", var.cidr_public))
    error_message = "The CIDR block must represent the IPv4 default route zero-address."
  }
}

variable "github_organization" {
  type        = string
  description = "The GitHub account organization"
  default     = "willfell"
}

variable "github_repository" {
  type        = string
  description = "The Github repository"
  default     = "balanced_brief"
}

variable "service" {
  type        = string
  description = "Used to name resources."
  default     = "BalancedBrief"
}

variable "common_tags" {
  type = map(any)
  default = {
    project = "BalancedBrief"
    owner   = "Will Fell"
  }
}

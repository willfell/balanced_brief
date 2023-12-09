variable "tags" {
  type = map(any)
  default = {
    project = "BalancedBrief"
    owner   = "Will Fell"
  }
}

variable "project" {
  default = "BalancedBrief"
}

variable "project_short_name" {
  default = "bf"
}

variable "instance_ami" {
  # Ubuntu 20.04
  default = "ami-087b37b6378c0c6d7"
}

variable "ssh_key_name" {
  default = "will_fell_mac_book"
}

variable "env" {
  default = "PROD"
}

variable "domain" {
  default = "balancedbrief.com"
}

variable "hostname" {
  default = "balancedbrief.com"
}

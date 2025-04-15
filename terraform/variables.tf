variable "rds-username" {
    description = "RDS username"
    type = string
    sensitive = true
}
variable "rds-password" {
    description = "RDS password"
    type = string
    sensitive = true
}

variable "aws-region" {
    description = "AWS region"
    type = string
    sensitive = true
}
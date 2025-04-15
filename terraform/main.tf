provider "aws" {
  region = var.aws-region
}

resource "aws_security_group" "db-app-con" {
  name_prefix = "db-app-con-"
  ingress {
    from_port   = 0
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "backend-test" {
    allocated_storage      = 20
    engine                 = "postgres"
    engine_version         = "17.2"
    identifier             = "backend-test"
    instance_class         = "db.t4g.micro"
    password               = var.rds-password
    skip_final_snapshot    = true
    publicly_accessible    = true
    username               = var.rds-username
    vpc_security_group_ids = [aws_security_group.db-app-con.id]
    apply_immediately = true
  }
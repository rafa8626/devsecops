provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "rafa-test1" {
  bucket        = "rafa-tf-bucket-1234567890"
  force_destroy = true
}

terraform {
  backend "s3" {
    bucket = "rafa-tf-bucket-1234567890"
    key    = "global/s3/terraform.tfstate"
    region = "eu-west-2"
  }
}

resource "aws_instance" "test-instance1" {
  ami           = "ami-0903ff18cc3c8e341"
  instance_type = "t2.micro"
  tags = {
    Name = "rafa-test-instance-${random_id.bucket_prefix.hex}"
  }
}

resource "random_id" "bucket_prefix" {
  byte_length = 8
}

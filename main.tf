provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "rafa-test1" {
  bucket        = "rafa-tf-bucket-1234567898"
  force_destroy = true
}

terraform {
  backend "s3" {
    bucket = "rafa-tf-bucket-1234567898"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "test-instance1" {
  ami           = "ami-0903ff18cc3c8e099"
  instance_type = "t2.micro"
  tags = {
    Name = "rafa-test-instance-${random_id.bucket_prefix.hex}"
  }
}

resource "random_id" "bucket_prefix" {
  byte_length = 8
}

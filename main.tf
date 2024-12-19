provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "test-tf-bucket-98765432112345"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_s3_bucket" "tf_test" {
  bucket = "test-tf-bucket-98765432112345"
}

resource "aws_instance" "test_instance" {
  ami           = "ami-01816d07b1128cd2d"
  instance_type = "t2.micro"
  tags = {
    Name = "rafa-test-instance-${random_id.bucket_prefix.hex}"
  }
}

resource "random_id" "bucket_prefix" {
  byte_length = 8
}

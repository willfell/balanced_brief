resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/20"

  tags = merge(var.tags)
}


resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags   = merge(var.tags)
}

resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.0.0/24" # Specify the CIDR block for your subnet
  availability_zone = "us-west-1a"
  tags              = merge(var.tags)
}

resource "aws_route_table" "public_routetable" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block                = "0.0.0.0/0"
    egress_only_gateway_id    = ""
    instance_id               = ""
    nat_gateway_id            = ""
    network_interface_id      = ""
    transit_gateway_id        = ""
    vpc_peering_connection_id = ""
    gateway_id                = aws_internet_gateway.internet_gateway.id
  }

  tags = merge(var.tags)
}

resource "aws_route_table_association" "public_rt_associations" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_routetable.id
}

resource "aws_eip" "eips" {
  vpc  = true
  tags = merge(var.tags)
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.eips.id
  subnet_id     = aws_subnet.public_subnet.id
  depends_on    = [aws_internet_gateway.internet_gateway]
  tags          = merge(var.tags)
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.1.0/24" # Specify the CIDR block for your subnet
  availability_zone = "us-west-1c"
  tags              = merge(var.tags)
}

resource "aws_route_table" "private_routetable" {
  vpc_id = aws_vpc.vpc.id
  tags   = merge(var.tags)
}

resource "aws_route" "route" {
  route_table_id         = aws_route_table.private_routetable.id
  destination_cidr_block = "0.0.0.0/0"
  depends_on             = [aws_route_table.private_routetable]
  nat_gateway_id         = aws_nat_gateway.nat_gateway.id
}

resource "aws_route_table_association" "private_rt_associations" {
  subnet_id      = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_routetable.id
}

resource "aws_default_security_group" "vpc_default_security_group" {
  vpc_id  = aws_vpc.vpc.id
  ingress = []
  egress  = []
  tags    = merge(var.tags)
}

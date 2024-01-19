resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/20"

  tags = merge(var.tags)
}


resource "aws_internet_gateway" "internet_gateway" {
  vpc_id = aws_vpc.vpc.id
  tags   = merge(var.tags, { Name = "internet-gateway" })
}

resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.0.0/24" # Specify the CIDR block for your subnet
  availability_zone = "us-west-1a"
  tags              = merge(var.tags, { Name = "public-subnet" })
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

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.1.0/24" # Specify the CIDR block for your subnet
  availability_zone = "us-west-1c"
  tags              = merge(var.tags, { Name = "private-subnet" })
}

resource "aws_route_table" "private_routetable" {
  vpc_id = aws_vpc.vpc.id
  tags   = merge(var.tags)
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

# Create Nat Instance stuff here - https://archive.kabisa.nl/tech/cost-saving-with-nat-instances/
# Reddit link with other info here - https://www.reddit.com/r/aws/comments/n6xyqz/comment/gx9rlvi/?utm_source=share&utm_medium=web2x&context=3

resource "aws_instance" "nat_instance" {
  ami                         = "ami-08d5c2c27495d734a" # AWS Linux 2
  instance_type               = "t2.micro"
  source_dest_check           = false
  subnet_id                   = aws_subnet.public_subnet.id
  associate_public_ip_address = true
  #key_name                    = var.ssh_key_name 
  key_name               = "will_fell_work_laptop"
  vpc_security_group_ids = [aws_security_group.nat_sg.id]
  root_block_device {
    volume_type           = "gp3" # Use gp3 which might be cheaper than gp2
    volume_size           = 8     # Size in GB. Adjust as needed but be cautious.
    delete_on_termination = true  # Ensures the volume is deleted when the instance is terminated.
  }
  user_data = base64encode(<<EOF
#!/bin/bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo /sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
EOF
  )

  tags = merge(var.tags, { Name = "nat-instance" })
}

resource "aws_security_group" "nat_sg" {
  name        = "nat-instance-sg"
  description = "Security group for NAT instance"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.allow_ssh.id, aws_security_group.ecs_tasks.id, aws_security_group.rds.id]
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_subnet.private_subnet.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags)
}

resource "aws_route" "private_subnet_nat_route" {
  route_table_id         = aws_route_table.private_routetable.id
  destination_cidr_block = "0.0.0.0/0"
  instance_id            = aws_instance.nat_instance.id
}


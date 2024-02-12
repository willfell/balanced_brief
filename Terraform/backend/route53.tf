data "aws_route53_zone" "zone" {
  name = var.domain
}

resource "aws_route53_record" "db_private" {
  zone_id = data.aws_route53_zone.zone.id
  name    = "db.${var.hostname}"
  type    = "A"
  ttl     = "300"
  records = [aws_instance.db.private_ip]
}

resource "aws_route53_record" "rds_db_private" {
  zone_id = data.aws_route53_zone.zone.id
  name    = "rds-db.${var.hostname}"
  type    = "CNAME"
  ttl     = "300"
  records = [aws_db_instance.bb_rds.address]
}

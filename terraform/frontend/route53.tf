data "aws_route53_zone" "zone" {
  name = var.domain
}

resource "aws_route53_record" "alias" {
  zone_id = data.aws_route53_zone.zone.id
  name    = var.hostname
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.origin.domain_name
    zone_id                = aws_cloudfront_distribution.origin.hosted_zone_id
    evaluate_target_health = true
  }
}

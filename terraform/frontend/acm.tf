resource "aws_acm_certificate" "cert" {
  provider          = aws.useast1
  domain_name       = var.hostname
  validation_method = "DNS"
}

resource "aws_route53_record" "cert_validation" {
  provider = aws.useast1
  name     = tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_name
  type     = tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_type
  zone_id  = var.hosted_zone_id
  records  = [tolist(aws_acm_certificate.cert.domain_validation_options)[0].resource_record_value]
  ttl      = 5
}

resource "aws_acm_certificate_validation" "cert" {
  provider                = aws.useast1
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [aws_route53_record.cert_validation.fqdn]
}

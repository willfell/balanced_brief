resource "aws_cloudfront_origin_access_identity" "origin" {}

resource "aws_cloudfront_distribution" "origin" {
  aliases             = [var.hostname]
  default_root_object = "index.html"
  enabled             = true
  is_ipv6_enabled     = true

  origin {
    domain_name = aws_s3_bucket.balanced_brief_frontend.bucket_regional_domain_name
    origin_id   = aws_s3_bucket.balanced_brief_frontend.bucket

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.origin.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    target_origin_id       = aws_s3_bucket.balanced_brief_frontend.bucket
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }
    #response_headers_policy_id = data.aws_cloudfront_response_headers_policy.cloudfront_response_headers_policy.id
  }



  # Those are required for VueJS history mode
  custom_error_response {
    error_caching_min_ttl = 10
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
  }
  custom_error_response {
    error_caching_min_ttl = 10
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn            = aws_acm_certificate_validation.cert.certificate_arn
    ssl_support_method             = "sni-only"
    minimum_protocol_version       = "TLSv1.2_2019"
    cloudfront_default_certificate = false
  }

  #   dynamic "logging_config" {
  #     for_each = var.enable_access_logs ? [aws_s3_bucket.log_bucket] : []
  #     content {
  #       bucket          = "${logging_config.value.id}.s3.amazonaws.com" # the ".s3.amazonaws.com" suffix is required for some reason."
  #       # Note: This configuration will automatically add the appropriate ACL to the destination bucket allowing c4c1ede66af53448b93c283ce9448c4ba468c9432aa01d700d3878632f77d2d0 to have R/W access
  #       include_cookies = false
  #       prefix          = var.stack_name
  #     }
  #   }
}

# data "aws_cloudfront_response_headers_policy" "cloudfront_response_headers_policy" {
#   name = "cloudfront-security-response-headers"
# }

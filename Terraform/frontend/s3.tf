data "aws_region" "current" {}

resource "aws_s3_bucket" "balanced_brief_frontend" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_ownership_controls" "ownership" {
  bucket = aws_s3_bucket.balanced_brief_frontend.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "balanced_brief_frontend_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.ownership]
  bucket     = aws_s3_bucket.balanced_brief_frontend.id
  acl        = "private"
}

resource "aws_s3_bucket_policy" "origin" {
  bucket = aws_s3_bucket.balanced_brief_frontend.id
  policy = data.aws_iam_policy_document.origin.json
}

data "aws_iam_policy_document" "origin" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.balanced_brief_frontend.arn,
      "${aws_s3_bucket.balanced_brief_frontend.arn}/*",
    ]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.origin.iam_arn]
    }
  }
}

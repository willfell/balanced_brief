resource "null_resource" "build_and_deploy" {
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = <<EOT
      cd ${path.module}/../../frontend/app/
      npm install
      npm run build
      cd build
      aws s3 sync . s3://${var.bucket_name}
      aws cloudfront create-invalidation --distribution-id ${aws_cloudfront_distribution.origin.id} --paths "/*"
    #   cd ..
    #   rm -rf build
    EOT
  }
  depends_on = [aws_cloudfront_distribution.origin]
}

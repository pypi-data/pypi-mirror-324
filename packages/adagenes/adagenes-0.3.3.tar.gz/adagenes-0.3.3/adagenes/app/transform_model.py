

def get_transform_model(output_format, request):

    transform_model = {}
    print("request ",request)

    if output_format == "vcf":
        transform_model["chrom"] = request.get("chrom")
        transform_model["pos"] = request.get("pos")
        transform_model["ref"] = request.get("ref")
        transform_model["alt"] = request.get("alt")

    return output_format, transform_model
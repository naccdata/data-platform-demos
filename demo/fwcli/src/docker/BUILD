file(name="entrypoint", source="entrypoint.sh")
docker_image(name='cli-uploader',
             source='Dockerfile',
             dependencies=[
                 ":entrypoint", "demo/fwcli/src/python/center_script:bin",
                 "demo/fwcli/src/python/pipeline_script:bin"
             ],
             image_tags=['0.0.1', 'latest'])

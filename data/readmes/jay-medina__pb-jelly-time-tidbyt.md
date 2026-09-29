# Peanut butter Jelly Time App for TidByt

- Tidbyt Dev Docs: https://tidbyt.dev/
- Starlark Docs: https://github.com/google/starlark-go/

## To Push to TidByt:
1) Render Image

    ```cli
    pixlet render pb_jelly_time.star
    ```

2) Push Image and Install app

    2a) Get the device ID

    2b) Push app to device
    ```
        pixlet push <Device_id> -i PBJellyTime pb_jelly_time.webp
    ```

## Demo
<img src="./pb_jelly_time.gif" width="80%">

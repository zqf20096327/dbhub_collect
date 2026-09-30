# website

### Brief Introduction

Website is openGauss community contents management system base on [Hugo](https://gohugo.io/) framework, [Universal Theme for Hugo](https://github.com/devcows/hugo-universal-theme) theme and [Hugo Book](https://github.com/alex-shpak/hugo-book) theme, maintained by this project [maintainers](#Maintainers), which publish on https://opengauss.org. Now we are under developing. you are welcome to join us.

### Installation

1. Build Image

```
docker build -t website:v0.0.1 .
```

2. Running in container

```
docker run -p 80:80 -d website:v0.0.1 > web.pid
```

The website will serving on http://your-server-ip:80

3. Stopping the container

```
docker rm -f `cat web.pid` && rm -f web.pid
```

### Debug

1. Install Hugo

```
curl -L https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_0.56.3_Linux-64bit.tar.gz | tar -xz && \
chmod +x hugo && mv hugo /usr/local/bin/
```

2. Run Hugo

```
hugo serve --bind 0.0.0.0 --port 80 --baseUrl /
```

The website will serving on http://your-server-ip:80, any change will take effect here.

### Contribution

1. Fork the repository
2. Create Feature_xxx branch
3. Commit your code
4. Create Pull Request

Please refer to [CONTRIBUTING](./CONTRIBUTING.md) for more guide.

### Get Help

- IRC： #opengauss-infra
- Mail: infra@opengauss.org

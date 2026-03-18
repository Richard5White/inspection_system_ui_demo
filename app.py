from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

# 后端地址
BACKEND_URL = "http://localhost:8080"


# =========================
# 页面路由
# =========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manufacturers")
def manufacturers():
    return render_template("manufacturers.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/batches")
def batches():
    return render_template("batches.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


# =========================
# API代理
# =========================

@app.route("/api/v1/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):

    url = f"{BACKEND_URL}/api/v1/{path}"

    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != "Host"},
        params=request.args,
        json=request.get_json(silent=True),
    )

    return Response(
        resp.content,
        resp.status_code,
        resp.headers.items()
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
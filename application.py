#!/usr/bin/env python3

from app import app, db


if __name__ == '__main__':

    app.run("0.0.0.0", port="8000", debug=True)

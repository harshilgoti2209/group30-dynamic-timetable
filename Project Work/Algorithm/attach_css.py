import numpy as np
import random
from copy import deepcopy
from gene import *


def template(self):
    return """
                <html>
                <head>
                    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
                    <script src="js/bootstrap.min..js"></script>
                    <link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100&display=swap" rel="stylesheet">
                    <link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300&display=swap" rel="stylesheet">
                </head>
                <body>
                <style>
                    *{
                        font-family: 'Roboto Slab', serif;
                    }
                    .title, table td{
                        text-align: center;
                    }
                    .title {
                        font-size: 24px;
                        font-family: cursive;
                        color: black;
                    }
                    table td{
                        height: 100px;
                        width: 200px;
                        padding: 30 10 30 10;
                        background-color: #e2eab4;
                    }
                    .teacher, .course{
                        display: block;
                    }
                    .no{
                        color: #965008;
                    }
                    .teacher{
                        font-weight: bold;
                        color: blue;
                    }
                    .course{
                        color: red;
                        font-size: 16px;
                    }
                    tr hr{
                        color: #fefefe;
                        padding-top: 5px;
                        padding-bottom: 5px;
                    }
                </style>
                    <div class = 'container'>{{timetable}}</div>
                </body>
                </html>
            """

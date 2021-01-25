import os
import json
import datetime


def main(event, context):
    body = """<style>
    .feedback {
    font-family:'Courier New', Courier, monospace;
    padding: 10px;
    background: #f2f2f2;
    color: #231f20;
    float: left;
    }
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    $(function() {
        $('#feedback-thx').hide();
    });
</script>
<script>
    function sendfeedback(value) {
        var FEEDBACK_URL = "%s";
        var site_url = (self===top) ? document.URL : document.referrer;
        var path = new URL(site_url).pathname;
        if (value == 1) {
            console.log("Helpful.");
        } else if (value == 0) {
            console.log("Not helpful.");
        } else {
            return 0;
        }
        $.post(FEEDBACK_URL, JSON.stringify({"value": value, "path": path}), function() {
            console.log("Sent feedback!");
        }, "json");
        $('.feedback').hide();
        $('#feedback-thx').show();
    }
</script>
<div id="feedback-container">
    <div class="feedback" id="feedback-pos" onclick="sendfeedback(1)">Helpful</div>
    <div class="feedback" id="feedback-neg" onclick="sendfeedback(0)">Not Helpful</div>
    <div class="feedback" id="feedback-thx">Thank you for your feedback!</div>
</div>"""

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*"
        },
        "body": body%os.environ.get("FEEDBACK_URL")
    }

    return response
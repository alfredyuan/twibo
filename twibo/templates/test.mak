<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Twibo - Backend</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="twibo weibo twitter" />
  <meta name="description" content="Twibo Backend System" />
  <link rel="shortcut icon" href="${request.static_url('twibo:static/favicon.ico')}" />
  <link rel="stylesheet" href="${request.static_url('twibo:static/twibo_backend.css')}" type="text/css" media="screen" charset="utf-8" />
  <script type="text/javascript" src="${request.static_url('twibo:static/jquery-1.9.1.min.js')}"></script>
  <script type="text/javascript" src="${request.static_url('twibo:static/twibo_backend.js')}"></script>
</head>
<body>
<div class="wrapper">
	<div class="main_content">
		<div class="header">
			<div id="logo_pic"><img src="${request.static_url('twibo:static/turbo-icon.gif')}"></div>
			<div class="float_left padding_ul_corner"><h1>Twibo Backend</h1></div>
			<hr class="clear" />
		</div>
	</div>
</div>
</body>
</html>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Twibo - Backend - Add Customer</title>
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
			<div class="padding_ul_10">
        		<ul class="nav_list">
          			<li><a href="/">Home</a></li>
          			<li><a href="/add">New Customer</a></li>
          			<li><a href="/engine">Twibo Engine Status</a></li>
        		</ul>
      		</div>
		</div>

		% if msg:
		<div class="notification padding_ul_20">
			<img src="${profile_pic}">
			<p class="padding_20">
				${msg}	
			</p>
		</div>
		% elif err_msg:
		<div class="error_msg">
			<p class="padding_20">
				${err_msg}
			</p>
		</div>
		%endif

		<div class="middle padding_20">
			<div class="add_form">
				<h2>New Customer</h2>
				<form name="add_customer" action="/add" method="post">
					Twitter Screen Name (ex. alfred_47):<br>
					<input type="text" name="tw_name" value="${params['tw_name'] if params else ""}"><br><br>
					Weibo Login Name (ex. y.haohan@gmail.com):<br>
					<input type="text" name="wi_name" value=${params['wi_name'] if params else ""}><br><br>
					Weibo Login Password:<br>
					<input type="text" name="wi_pwd" value=${params['wi_pwd'] if params else ""}><br><br>
					Automatically Syndicating:<br>
					<input type="radio" name="auto_sync" value="True" checked>&nbsp;True<br>
					<input type="radio" name="auto_sync" value="False">&nbsp;False<br><br>
					<p class="remark">If you want to turn on Auto-sync, please ensure weibo account name and password have been correctly inputed.</p><br>
					<input type="submit" value="Submit">
				</form>
			</div>
		</div>

		<div class="footer">
			<hr class="clear"/>
			Twibo 1.0
		</div>
	</div>
</div>
</body>
</html>


#!/usr/bin/perl

#----------------------------------------------------------------------
#	 �ذ����� �ʿ��ϴ� ���� 2 ver 3.00b (Free)
#	 AUTHOR	: ��
#	 E-MAIL	: osktaka@hotmail.com
#	 URL	: http://homepage2.nifty.com/osktaka/
#
#          �ѱ۹��� : jjangg96@hanmail.net
#          �ѱ۹��� : http://www.x2-dr.com
#
#	�� ��ũ��Ʈ�� �����Դϴٸ�, ��� �̿��� ����, �� ������� �������� �����Ƿ� ������ �ֽʽÿ�.
#	��ũ��Ʈ�� ���� ������"��"���� ��Ź�մϴ�.
#	�� ��ũ��Ʈ�� ����� �Ͼ�� �Ǵ� ������ å���� ���� �ʽ��ϴ�.
#	�� ��ũ��Ʈ�� �Ʒ��� �̿� ������ ���� �����ǰ� �ֽ��ϴ�.
#	http://homepage2.nifty.com/osktaka/down/down_top.htm
#
#	�� ������ �۹̼���,
#	Ȯ����(extension)��. cgi�� ���� 755,. dat�� ���� 666,. ini�� ���� 644�Դϴ�.
#
#----------------------------------------------------------------------


$| = 1;
require './jcode.pl';
require './gekipawa.ini';

########## ���� ���� ����
sub kankyou{

$totpoint		= '200';		# ���� �Ķ���� �ִ�ġ

#### ������ ����Ʈ�� ���
if($icon_use){
	$i = 0;
	@iconlist = ();
	foreach(@icon2) {
		push @iconlist, "<option value=\"$icon1[$i].gif\">$_\n";
		$i++;
	}
}

$body = "<body bgcolor=\"$bgcolor\" text=\"$text\" alink=\"$alink\" link=\"$link\" vlink=\"$vlink\" background=\"$imgurl/$background\">";

}#end kankyou

&kankyou;
&decode;
&readlog;

if($mente){ &error('����Ʈ�ͽ����Դϴ�. ��� ��ٷ� �ּ���. '); }

# ��� ó��
	if($form{'record'})	{ &record; }
	if($form{'comment'}){ &comsyori; }
	if($form{'delete'})	{ require './geki_login.cgi'; &delete; }
	if($form{'comdel'})	{ &comdelete; }

	if($form{'mode'} eq 'game_log')	 { &game_log; exit; }
	if($form{'mode'} eq 'icon_table'){ &icon_table; exit; }

	if($form{'sinki_make'})	{ &sinki_make; exit; }
	if($form{'make_end'})	{ &make_end; exit; }
	if($form{'kanri'})		{ &kanri; exit; }

	if($form{'login'})		{ require './geki_login.cgi'; &login; exit; }
	if($form{'camp_end'})	{ require './geki_login.cgi'; &camp_rec; &login; exit; }
	if($form{'delekaku'})	{ require './geki_login.cgi'; &delekaku; exit; }

	if($form{'playkaku'})	{ require './geki_login.cgi'; &playkaku; exit; }
	if($form{'campin'})		{ require './geki_login.cgi'; &campin; exit; }
	if($form{'playball'})	{ require './geki_game.cgi'; &playlog; exit; }

	if($form{'league_rank'}){
		require './geki_else.cgi';
		$no = $form{'no'};
		if($no eq 1){ &play_rank; }
		else		{ &team_rank; }
		exit;
	}
	if($form{'point_rank'})	{ require './geki_else.cgi'; &point_rank; exit; }

	if($form{'kiroku'}){
		require './geki_else.cgi';
		$no = $form{'no'};
		if($no eq 1)				{ &last_team; }
		elsif($no eq 2)				{ &last_play; }
		elsif($no eq 3)				{ &past_rank; }
		elsif($no eq 4 || $no eq 5)	{ &each_reco; }
		else						{ &last_kekka; }
		exit;
	}

	if($form{'rule'})		{ &rule; exit; }

&top;

exit;


##### ���ڵ壦���� ������ �ְ� �޾�
sub decode{

#�Էµ� ���� ���ڵ�
	if ($ENV{'REQUEST_METHOD'} eq "GET") {
		$buffer = $ENV{'QUERY_STRING'};
	} elsif ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($key, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value, "euc");
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/ //g;
	$value =~ s/ //g;
	$form{$key} = $value;

	}

}#end decode

##### �α� read
sub readlog{

# �ð��� ���
	
	$times = time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$years = sprintf("%02d",$years + 1900);
	$month = sprintf("%02d",$mon + 1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$sec = sprintf("%02d",$sec);

# ������ ���� ó��
	open(PR,"$past_rankfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(PR,0,0);  @past_rank = <PR>;  close(PR);
	($pr_date, $pr_dai) = split(/<d>/, $past_rank[0]);

	if(!$past_rank[0]){
		$kakiko_times = $times - ((($hour - $league_time + 24) % 24 ) * 3600 + $min * 60 + $sec);
		$kakiko = "$kakiko_times<d>0<d><d><d><d>\n";
		$league_day = 1;

		open(PR,">>$past_rankfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
			eval 'flock(PR,2);';
			seek(PR,0,0);	print PR $kakiko;
		close(PR);
			eval 'flock(PR,8);';
	}elsif($pr_dai eq -1){
		&error('���� ���� ó�����Դϴ�. ��а� ��ٸ��� �־��');
	}else{
		$league_day = int(($times - $pr_date) / (60 * 60 * 24)) + 1;
	}

	if($league_day > $league_limit){ require './geki_else.cgi'; &league_end; $league_day = 1; }

	$kitei_hit = $league_day * 25;
	$kitei_pit = $league_day * 25;

	$pr_dai++;
	$league_dai = "<font size=4>��<b>$pr_dai</b>ȸ</font>";

}#end readlog

##### ��� ǥ��
sub header{

	print "Content-type: text/html\n\n";#����Ʈ Ÿ�� ���
	print <<"_EOF_";
<html>
<head>
<title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=euc-kr">
<STYLE type="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score			{ font-size: 10pt; color: #FFFFFF; background-color: #008800 }
-->
</STYLE>
</head>
$body
<center>
<!--���� ��� ���� ��ġ, ������ ���-->

_EOF_

}#end header

##### ǲ�� ǥ��
sub footer{

	print <<"_EOF_";
<br><br>
<form action="$cgifile" method="$method">
<table cellpadding="3">
	<tr>
	<td bgcolor="$iroformwaku">
	<input type="submit" value="$mestop">
	<input type="submit" name="league_rank"	value="$mesrank">
	<input type="submit" name="point_rank"  value="$mespoint_rank">
	<input type="submit" name="kiroku"		value="$meskiroku">
	<input type="submit" name="rule"		value="$mesrule">
	<input type="button" value="$meshome" onClick="top.location.href='$url'">
	</td>
	</tr>
</table>
</form>

_EOF_

}#end footer

##### ���۱� ǥ��
sub chosaku{

	print <<"_CHOSAKU_";
</center>
<hr size="1">
<div align="right"><a href="http://homepage2.nifty.com/osktaka/" target="_blank"><font size="2">�ذ����� �ʿ��ϴ� ���� 2 ver 3.00b (Free)</font></a></div>
<div align="right"><a href="http://www.x2-dr.com/" target="_blank"><font size="2">X2-DR.com ������ Ŀ�´�Ƽ : �ѱ��� ����
<div align="right"><a href="http://www.watsescape.com/" target="_blank"><font size="2">������ ��� : �Ŀ� ����
</font></a></div>
<!--���� ��� ���� ��ġ, ������ �Ϻ�-->
</body>
</html>
_CHOSAKU_

}#end chosaku

##### ���� ���� ǥ��
sub top1{

	if($league_day eq 1){
		$l_day_pri = "��<font size=6 color=\"FF0000\"><b> ù�� </b></font>��";
	}elsif($league_day eq $league_limit){
		$l_day_pri = "��<font size=6 color=\"FF0000\"><b> ������ �� </b></font>��";
	}else{
		$l_day_pri = "��<font size=6 color=\"FF0000\"><b> $league_day </b></font><font size=4>��°</font>��";
	}
	$l_day_pri = "$l_day_pri<br>(���� ����$league_time�÷� �ٲ�ϴ�)";

	print <<"_EOF_";
	<br>
	$league_dai<font size=4> �ذ����� �ʿ��ϴ� ���� 2</font><br>
	$l_day_pri<br><br>

_EOF_

	if($bbs_mode){
		print "[ <a href=$bbs_url target=_blank>$bbs_name</a> ]<br><br>\n";
	}

}#end top1

##### ž ������
sub top{

	open(US,"$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	@icon_pri = ();
	for($i=0; $i<3; $i++){
		($saku[$i], $pass[$i], $home[$i], $team[$i], $icon[$i], $date[$i], $ip[$i], $teamdata[$i]) = split(/<p>/, $users[$i]);
		($lastjun[$i], $win[$i], $wincon[$i], $winmax[$i], $lose[$i]) = split(/<>/, $teamdata[$i]);
		if($home[$i]){ $saku[$i] = "<a href=\"$home[$i]\" target=\"_blank\">$saku[$i]</a>"; }
	}

	if($icon_use)	{ $icon_pri[0] = "<img src=\"$imgurl/$icon[0]\"></td><td><font size=5 color=\"FF0000\"><b>$team[0]</b></font><br>"; }
	else			{ $icon_pri[0] = "<font size=5 color=\"FF0000\"><b>$team[0]</b></font>"; }

	$sinki = '';
	if($#users+1 < $team_max){
		$sinki = "����<input type=submit name=sinki_make value=\"NEW\">";
	}

# è�Ǿ�
	open(WN,"$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(WN,1);';
	seek(WN,0,0);  @winners = <WN>;  close(WN);
	eval 'flock(WN,8);';

	($saku, $d, $home, $team, $icon, $date, $d, $teamdata) = split(/<p>/, $winners[0]);
	($lastjun, $win, $wincon, $winmax, $lose) = split(/<>/, $teamdata);
	if($home){ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a>"; }
	if($icon_use)	{ $icon_pri[1] = "<img src=\"$imgurl/$icon\" align=\"absmiddle\"><font size=4 color=\"008000\"><b>  $team</b></font>"; }
	else			{ $icon_pri[1] = "<font size=4 color=\"008000\"><b>$team</b></font>"; }

	@champ_pri = ();
	$champ_pri[0] = "<table border=1 width=100% cellspacing=0 cellpadding=5>\n";
	$champ_pri[1] = "<tr align=center>\n";
	$champ_pri[2] = "<td><font size=5 color=\"DD9966\"><B>Now Champion! </B></font> (����<font color=\"FF0000\" size=7><B>$wincon</B></font>������!  )<br>\n";
	$champ_pri[3] = "$icon_pri[1] <br>�� ���� : $saku ��$win�� $lose��\n";
	$champ_pri[4] = "<br></td></tr></table>\n";

# �ֱ��� ����
	open(LG,"$leaguefold/$logfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(LG,0,0);  @glog = <LG>;  close(LG);

	@game_pri = ();
	$game_pri[0] = "<table border=1 width=100% cellspacing=0 cellpadding=5><tr align=center><td>�ֱ� 5 ������ ���</td></tr>\n";

	for($i=0; $i<5; $i++){
		($g_date, $g_kekka) = split(/<>/, $glog[$i]);
		if($g_date){
			if($i < 3){
				$game_pri[$i+1] = "<tr align=center><td><a href=\"$cgifile?mode=game_log&no=$i\">$g_kekka</a></td></tr>\n";
			}else{
				$game_pri[$i+1] = "<tr align=center><td>$g_kekka</td></tr>\n";
			}
		}else{
			$game_pri[$i+1] = "<tr align=center><td> - </td></tr>\n";
		}
	}
	$game_pri[6] = "</table>\n";

# �ڸ�Ʈ
	open(CF,"$commentfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	@com_pri = ();
	$com_pri[0] = "<table border=1 width=\"$ysize\" cellpadding=5 cellspacing=0>\n";
	$com_pri[1] = "<tr align=\"center\"><td>���� ���� ���� �ڸ�Ʈ</td></tr>\n";
	$com_pri[2] = "<tr><td bgcolor=\"FFFFFF\">\n";

	$i = 0;
	foreach(@comments){
		($no, $saku, $home, $date, $com, $kekka) = split /<>/;
		$date = &date($date);
		if($home){ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a> "; }
		if($no){
			if($kekka){ $kekka = "�� $kekka ��"; }
			$com_pri[$i+3] = "�� ���״��� �� �� $com �� $kekka ($date) \n";
		}else{
			$com_pri[$i+3] = "�� $saku �� �� $com �� �� $kekka �� ($date) \n";
		}

		if($i ne $#comments){
			$com_pri[$i+3] = "$com_pri[$i+3]<hr width=\"70%\" size=1>\n";
		}
		$i++;
	}
	$com_pri[$#comments+4] = "</table>\n";

	&get_cookie;
	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$title</font><br>
<br>$top_comment

_EOF_

	&top1;

    $c_home =~ s/http:\/\///g;	# �ּ��� ó��

	print <<"_EOF_";
<table width=$ysize cellpadding=10>
	<tr align=center>
	<td width=75%>
	<font size=5 color="008000"><b>�� ���� ��Ȳ ��</b></font><br>
	<table border=1 width="100%" cellspacing=0 cellpadding=5>
		<tr align=center>
		<td><font color="#FF0000" size=5><b>����</b></font></td>
		<td>
		<table border=0 width=70%>
			<tr align=center>
			<td>$icon_pri[0]
			<font size=3>($saku[0])<br>$win[0]�� $lose[0]��</font>
			</td></tr>
		</table>
		</td></tr>
		<tr align=center>
		<td><font size=4><b>2��</b></font></td>
		<td><font size=4><b>$team[1]</b></font>($saku[1])<br>$win[1]�� $lose[1]��</font>
		</td></tr>
		<tr align=center>
		<td><b>3��</b></td>
		<td><b>$team[2]</b>($saku[2])<br>$win[2]�� $lose[2]��</font>
		</td></tr>
	</table>
	</td>
	<td width=30%>

	<table border=1 width=100% cellspacing=0 cellpadding=5>
		<tr align=center>
		<td>
		<br>$userlimit �ϰ� ������ ���� ������, ���� �����ʹ� �Ұŵ˴ϴ�.<br><br>

		<form action=$cgifile method=$method>
		<table width=170>
			<tr>
			<td width=75>�̸�</td>
			<td width=95><input type=text name=saku size=15 value=$c_saku></td>
			</tr><tr>
			<td width=75>�н�����</td>
			<td width=95><input type=password name=pass size=10 value=$c_pass></td>
			</tr>
		</table>
		<br>
		<input type=submit name=login value="Enter">
		$sinki
		</form>
		</td>
		</tr>
	</table>

	</td></tr>
	<tr align=center>
	<td width=75%>
	@champ_pri
	</td>
	<td width=25%>
	@game_pri
	</td>
	</tr>
</table>
<br><br>
@com_pri
<br>

_EOF_

	&footer;

	print <<"_EOF_";
<div align=right>
<form action=$cgifile method=$method>
<input type=password name=kanripass size=10>
<input type=hidden name=kanri value=1>
<input type=submit name=kanri value="������">
</form>

_EOF_

	&chosaku;

}#end top

##### �ű� ��� ȭ��
sub sinki_make{

	@bonuslist = ();
	foreach(1..10) {
		if($_ eq 5){
			push @bonuslist, "<option value=$_ selected>$_\n";
		}else{
			push @bonuslist, "<option value=$_>$_\n";
		}
	}
	@positlist = ();
	@position = ('����','1���','2���','3���','���ݼ�','���ͼ�','�߰߼�','���ͼ�');
	foreach(@position) {
		push @positlist, "<option value=$_>$_\n";
	}
	if($icon_use)	{ $icon_pri = "<tr><td>������</td><td><select name=\"icon\">@iconlist</select> [ <a href=\"$cgifile?mode=icon_table\" target=\~_blank\">������ �϶�</a>  ]</td></tr>"; }
	else			{ $icon_pri = ''; }

	&header;
	&java_sum;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">�ű� ���</font>

<form action="$cgifile" method="$method">
<input type="submit" value="ó��ȭ������ ���ƿ´�">
</form>
<br>
<form action="$cgifile" method="$method" name=para>
<table border=1 width=$ysize cellpadding=5>
	<tr>
	<td width=60%>
	<br>
	<table width=100%>
		<tr>
		<td>���� �̸�</td>
		<td><input type=text name=team size=15>(�ѱ�,����<B>$nameleng</B>�ڱ���)</td>
		</tr>
		$icon_pri
		<tr>
		<td>����� �̸�</td>
		<td><input type=text name=saku size=15>(�ѱ�,����<B>$nameleng</B>�ڱ���)</td>
		</tr>
		<tr>
		<td valign=top>Ÿ��<br>(1:�� - 10:��)</td>
		<td>
		<table border=1 cellspacing=0>
			<tr align=center>
			<td>���� �ǽ�</td>
			<td>��Ʈ</td>
			<td>����</td>
			<td>������ �ǽ�</td>
			</tr>
			<tr align=center>
			<td><select name=b_act>@bonuslist</select></td>
			<td><select name=b_bnt>@bonuslist</select></td>
			<td><select name=b_ste>@bonuslist</select></td>
			<td><select name=b_mnd>@bonuslist</select></td>
			</tr>
		</table>
		</td>
		</tr>
		<tr>
		<td>Ȩ ������</td>
		<td><input type=text name=home size=30 value="http://"></td>
		</tr>
		<tr>
		<td>�н�����</td>
		<td><input type=password name=pass size=10>(����,����<b>$passleng</b>�ڱ���)</td>
		</tr>
	</table>
	<br>
	</td>
	<td width=40% align=center>

_EOF_

	&parasum_pri;

	print <<"_EOF_";
	<br>
	<input type=submit name=make_end value="���">
	</td>
	</tr>
</table>
<br>
<br>

_EOF_

	&make_table;

	print "</form><br><br>\n";

	&chosaku;

}#ens sinki_make

##### �ɷ�ġ �հ� ǥ��
sub parasum_pri{

	print <<"_EOF_";

	�� �����ɷ�ġ�� ���� ��� ��<br><br>
	<table>
		<tr>
		<td>���� �����ɷ�ġ�� �հ��</td>
		<td><b>$para_min</b>~<b>$para_max</b></td>
		</tr>
		<tr>
		<td>���� ��ü�� �հ��<b>$totpoint</b></td>
		<td><strong>���磺</strong><input type=text value=$totpoint name=para_t size=4></td></tr>
		<tr>
		<td>���Ķ����<b>10</b>�� ����<b>$ten_max</b>��</td>
		<td><strong><font color="#FF0000">����</font>��</strong><input type=text value=0 name=para_10 size=2></td></tr>
		<tr>
		<td>���Ķ����<b>8</b>~<b>9</b>�� ����<b>$eight_max</b>������</td>
		<td><strong><font color="#0000FF">����</font>��</strong><input type=text value=0 name=para_89 size=2></td></tr>
	</table>

_EOF_

}#end parasum_pri

##### �ɷ�ġ �հ� JavaScript
sub java_sum{

	if($form{'sinki_make'}){
		if($icon_use){
			@base = (15,70,19,74);
		}else{
			@base = (14,69,18,73);
		}
	}else{
		@base = (6,61,10,65);
	}
	print <<"_EOF_";
<script laguage="Javascript">
<!--
	var ten;
	var etnn;

function selectCahnge() {
	frmsta = new Array(39);
	stam = new Array(9);

	var t_total = 0;
	ten = 0;
	etnn = 0;

	for (i=0; i<10; i++) {
		stam[i] = 0;
		for (j=0; j<4; j++) {
			if(i < 8){
				x = i * 7 + j + $base[0];
			}else{
				x = (i - 8) * 6 + j + $base[1];
			}
			y = i * 4 + j;
			frmsta[y] = parseInt(document.para.elements[x].value);
			stam[i] += frmsta[y];
			ten_check(frmsta[y]);
		}
		t_total += stam[i];
	}
	for (i=0;i<10;i++) {
		if(i < 8){
			x = i * 7 + $base[2];
		}else{
			x = (i - 8) * 6 + $base[3];
		}
		document.para.elements[x].value = stam[i];
	}
	document.para.para_t.value = t_total;
	document.para.para_89.value = etnn;
	document.para.para_10.value = ten;
}

function ten_check(tmp_c) {
	if (tmp_c > 7) {
		if (tmp_c == 10) { ten++; }
		if (tmp_c == 9) { etnn++; }
		if (tmp_c == 8) { etnn++; }
	}
}
// -->
</script>

_EOF_

}#end Java_sum

##### ���� ��� ���̺�
sub make_table{

	print "���� ��ġ�� �����ϰ�, �̸��� 4���� �ɷ�ġ�� ������ �ּ���. \n";
	print "<table border=1 width=90%>\n";

	for($i=0; $i<10; $i++){
		$jun = $i + 1;
		if($form{'sinki_make'}){
			@{$positlist[$i]} = @positlist;
			$name_value = '';
			$para1[$i] = $para2[$i] = $para3[$i] = $para4[$i] = 5;
			$parasum[$i] = 20;
		}else{
			$name_value = "value=$p_name[$i]";
		}
		if($i eq 0){
			print "<tr align=center><td rowspan=9>Ÿ��</td>\n";
			print "<td>Ÿ��</td><td>��ġ</td><td>�̸�(�ѱ�,����<b>5</b>�ڱ���)</td><td>�Ŀ�</td><td>��Ȯ��</td><td>�޸���</td><td>�����</td><td><b>�հ�</b></td></tr>\n";
		}elsif($i eq 8){
			print "<tr align=center><td rowspan=3>����</td>\n";
			print "<td>Ÿ��</td><td>��ġ</td><td>�̸�</td><td>�ӱ�</td><td>��ȭ��</td><td>������</td><td>�����</td><td><b>�հ�</b></td></tr>\n";
		}
		print "<tr align=center><td>$jun</td>\n";
		if($i < 8){
			print "<td><select name=posit$i>@{$positlist[$i]}</select></td>\n";
		}else{
			print "<td>����</td>\n";
		}
		print "<td><input type=text name=p_name$i $name_value size=10></td>\n";
		print "<td><input type=text name=para1_$i value=$para1[$i] size=2 onChange=\"selectCahnge()\"></td>\n";
		print "<td><input type=text name=para2_$i value=$para2[$i] size=2 onChange=\"selectCahnge()\"></td>\n";
		print "<td><input type=text name=para3_$i value=$para3[$i] size=2 onChange=\"selectCahnge()\"></td>\n";
		print "<td><input type=text name=para4_$i value=$para4[$i] size=2 onChange=\"selectCahnge()\"></td>\n";
		print "<td><input type=text name=para_c$i value=$parasum[$i] size=3></td></tr>\n";
	}
	print "</table>\n";

}#end make_table

##### ��� Ȯ�� ȭ��
sub make_end{

	$saku		= $form{'saku'};
	$pass		= $form{'pass'};
	$home		= $form{'home'};
	$team		= $form{'team'};
	$icon		= $form{'icon'};

# �̸��� ���� üũ
	if((length($team) < 1) || (length($team) > $nameleng *2)){ &error("�̸��� ���̴�$nameleng �ڱ��� ��. "); }
	if((length($saku) < 1) || (length($saku) > $nameleng *2)){ &error("�̸��� ���̴�$nameleng �ڱ��� ��. "); }

# ����Ʈ ȣ��Ʈ ���
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# �̸��������� �ߺ� üũ
 	open(US,"$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	foreach(@users){
		($checksaku,$checkpass,$d,$checkteam,$d,$d,$checkip) = split /<p>/;
		if($saku eq $checksaku){
			&error('�� �������� ���� ���ǰ� �ֽ��ϴ�. ');
		}
		if($team eq $checkteam){
			&error('�� ������ ���� ���ǰ� �ֽ��ϴ�. ');
		}
		if($host eq $checkip && $double_check){
			&error('���� ���� ����� �� �� ����. ');
		}
	}

	@bosspara	= ($form{'b_act'},$form{'b_bnt'},$form{'b_ste'},$form{'b_mnd'});

	&chara_para;

	&header;

	print <<"_EOF_";
<font color=$tcolor size=$tsize>��� Ȯ��</font>
<br><br>�̰����� ����մϴ�. �����ϱ�? <br>(���ƿ� ���� �������� �ڷΰ���΢�)<br><br>

<form action=$cgifile method=$method>
<input type=hidden name=record value=1>

_EOF_

	for($i=0; $i<10; $i++){
		print "<input type=hidden name=posit$i  value=$posit[$i]>\n";
		print "<input type=hidden name=p_name$i value=$p_name[$i]>\n";
		print "<input type=hidden name=para1_$i value=$para1[$i]>\n";
		print "<input type=hidden name=para2_$i value=$para2[$i]>\n";
		print "<input type=hidden name=para3_$i value=$para3[$i]>\n";
		print "<input type=hidden name=para4_$i value=$para4[$i]>\n";
	}
	print "<input type=hidden name=team value=\"$team\">\n";
	print "<input type=hidden name=icon value=\"$icon\">\n";
	print "<input type=hidden name=saku value=\"$saku\">\n";
	print "<input type=hidden name=home value=\"$home\">\n";
	print "<input type=hidden name=pass value=\"$pass\">\n";
	print "<input type=hidden name=b_act value=\"$bosspara[0]\">\n";
	print "<input type=hidden name=b_bnt value=\"$bosspara[1]\">\n";
	print "<input type=hidden name=b_ste value=\"$bosspara[2]\">\n";
	print "<input type=hidden name=b_mnd value=\"$bosspara[3]\">\n";

	print "<input type=submit name=login value=\"��� �Ϸ�\"></form>\n";

	&touroku_table;
	&chosaku;

}#end make_end

##### ĳ���͸����� �Ķ����
sub chara_para{

# �н����� üũ
	if((length($pass) < 4) || (length($pass) > $passleng)){ &error("�н������� ���̴� 4~$passleng �ڱ��� ��. "); }

#HP�� ����
	($home =~ /^http:\/\/[a-zA-Z0-9]+/) || ($home = '');

	for($i=0; $i<10; $i++){
		$posit[$i]	= $form{"posit$i"};
		$p_name[$i]	= $form{"p_name$i"};
		$para1[$i]	= $form{"para1_$i"};
		$para2[$i]	= $form{"para2_$i"};
		$para3[$i]	= $form{"para3_$i"};
		$para4[$i]	= $form{"para4_$i"};
	}
# �� ĳ������ üũ
	for($i=0; $i<10; $i++){
		if(length($p_name[$i]) < 1 || length($p_name[$i]) > 5 * 2){ &error('������ �̸��� ���̴� 5 �ڱ��� ��. '); }
		for($j=0; $j<$i; $j++){
			if($i < 9 && $posit[$i] eq $posit[$j]) { &error('�������� �ߺ� �ǰ� �־�. '); }
			if($p_name[$i] eq $p_name[$j]){ &error('������ �̸��� �ٸ� �̸����� ��. '); }
		}
	}

# �ɷ�ġ üũ
	$totalpoint	= 0;
	$check1		= 0;
	$check2		= 0;
	for($i=0; $i<10; $i++){
		if(($para1[$i] < 1 || $para2[$i] < 1 || $para3[$i] < 1 || $para4[$i] < 1) || ($para1[$i] > 10 || $para2[$i] > 10 || $para3[$i] > 10 || $para4[$i] > 10)){
			&error('���������� �Ķ���ʹ� 1~10���� ��. ');
		}
		if(int($para1[$i]) ne $para1[$i] || int($para2[$i]) ne $para2[$i] || int($para3[$i]) ne $para3[$i] || int($para4[$i]) ne $para4[$i]){
			&error('�Ķ���ʹ� ������ ��. ');
		}
		$totalcheck = $para1[$i] + $para2[$i] + $para3[$i] + $para4[$i];
		if($totalcheck < $para_min || $totalcheck > $para_max){ &error("���������� �Ķ������ �հ��$para_min~$para_max�� ��. "); }
		else{ $totalpoint += $totalcheck; }

		if($para1[$i] >= 8){ $check1++; }
		if($para2[$i] >= 8){ $check1++; }
		if($para3[$i] >= 8){ $check1++; }
		if($para4[$i] >= 8){ $check1++; }
		if($para1[$i] eq 10){ $check2++; $check1--; }
		if($para2[$i] eq 10){ $check2++; $check1--; }
		if($para3[$i] eq 10){ $check2++; $check1--; }
		if($para4[$i] eq 10){ $check2++; $check1--; }
	}

	if($check2 > $ten_max)  { &error('�Ķ���� 10�� ���� ����. '); }
	if($check1 > $eight_max){ &error('�Ķ���� 8~9�� ���� ����. '); }
	if($totalpoint ne $totpoint){ &error("�Ķ������ �հ谡$totpoint�� ���� �ʾҾ�. "); }

}#end chara_para

##### ��� ��� ���̺�
sub touroku_table{

	if($icon_use)	{ $icon_pri = "<img src=\"$imgurl/$icon\">"; }
	else			{ $icon_pri = "<br>NO ICON<br><br>"; }

	print <<"_EOF_";
<br>
<table width="$ysize">
	<tr align="center">
	<td width="35%">
	<table border=0 width=120 cellpadding=3 >
		<tr align=center>
		<td>
		$icon_pri
		</td>
		</tr>
	</table>
	</td>
	<td width=65%>
	<table width="90%">
		<tr>
		<td width=100>���� �̸�</td>
		<td>$team</td>
		</tr>
		<tr>
		<td width=100>����� �̸�</td>
		<td>$saku</td>
		</tr>
		<tr>
		<td valign=top>Ÿ��<br>(1:�� - 10:��)</td>
		<td>
		<table border=1 cellspacing=0>
			<tr align=center>
			<td>���� �ǽ�</td>
			<td>��Ʈ</td>
			<td>����</td>
			<td>������ �ǽ�</td>
			</tr>
			<tr align=center>
			<td>$bosspara[0]</td>
			<td>$bosspara[1]</td>
			<td>$bosspara[2]</td>
			<td>$bosspara[3]</td>
			</tr>
		</table>
		</td></tr>
		<tr>
		<td width=100>Ȩ ������</td>
		<td>$home</td>
		</tr>
		<tr>
		<td width=100>�н�����</td>
		<td>$pass</td>
		</tr>
	</table>
	</td>
	</tr>
	<tr align="center">
	<td colspan=2>
	<table border="1" width="90%">

_EOF_

	for($i=0; $i<10; $i++){
		if($form{'make_end'}){
			$condition = "����";
		}else{
			if($cond[$i] < 2)	{ $condition = "�־�"; }
			elsif($cond[$i] < 4){ $condition = "���ڴ�"; }
			elsif($cond[$i] < 6){ $condition = "����"; }
			elsif($cond[$i] < 8){ $condition = "ȣ��"; }
			else				{ $condition = "��ȣ"; }
		}

		if($i eq 0){
			print "<tr align=center><td rowspan=9>Ÿ��</td>\n";
			print "<td>����</td><td>��ġ</td><td>�̸�</td><td>����</td><td>�Ŀ�</td><td>��Ȯ��</td><td>�޸���</td><td>�����</td></tr>\n";
		}elsif($i eq 8){
			print "<tr align=center><td rowspan=3>����</td>\n";
			print "<td>����</td><td>��ġ</td><td>�̸�</td><td>����</td><td>�ӱ�</td><td>��ȭ��</td><td>������</td><td>�����</td></tr>\n";
		}
		$jun = $i + 1;
		print "<tr align=center><td>$jun</td>\n";
		if($i < 8){
			print "<td>$posit[$i]</td>\n";
		}else{
			print "<td>����</td>\n";
		}
		print "<td>$p_name[$i]</td>\n";
		print "<td>$condition</td>\n";
		print "<td>$para1[$i]</td>\n";
		print "<td>$para2[$i]</td>\n";
		print "<td>$para3[$i]</td>\n";
		print "<td>$para4[$i]</td></tr>\n";
	}
	print "</table></td></tr></table><br><br>\n";

}#end touroku_table

##### �� ��� ó��
sub record{

# ������ �Űܳ��´�
	$saku		= $form{'saku'};
	$pass		= $form{'pass'};
	$home		= $form{'home'};
	$team		= $form{'team'};
	$icon		= $form{'icon'};

# ����Ʈ ȣ��Ʈ ���
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# �α׿� �����ϴ� ��Ÿ���� ����
	@players = ();
	for($i=0; $i<10; $i++){
		$id = $jun = $i + 1;
		$posit	= $form{"posit$i"};
		$p_name	= $form{"p_name$i"};
		$para1	= $form{"para1_$i"};
		$para2	= $form{"para2_$i"};
		$para3	= $form{"para3_$i"};
		$para4	= $form{"para4_$i"};
		if($i < 8){
			$players[$i] = "$id<>$jun<>$posit<>$p_name<>5<>$para1<>$para2<>$para3<>$para4<>0<>0<>0<>0<>0<>0<>0<>0";
		}else{
			$players[$i] = "$id<>$jun<>����<>$p_name<>5<>$para1<>$para2<>$para3<>$para4<>0<>0<>0<>0<>0<>0<>0";
		}
	}
	$players = join('<c>', @players);

	$teamdata  = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0";
	$pointdata = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0";
	$bosstype = "$form{'b_act'}<>$form{'b_bnt'}<>$form{'b_ste'}<>$form{'b_mnd'}";
	$kakiko = "$saku<p>$pass<p>$home<p>$team<p>$icon<p>$times<p>$host<p>$teamdata<p>$pointdata<p>$bosstype<p>$players<p><p>0<p>\n";

# ���� ���Ͽ��� ������
	open(US,"+<$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(US,2);';

	@users = <US>;
	if($double_check){
		foreach(@users){
			($checksaku,$checkpass,$d,$checkteam,$d,$d,$checkip) = split /<p>/;
			if($host eq $checkip){
				&error('���� ���� ����� �� �� ����. ');
			}
		}
	}
	push(@users,$kakiko);

	truncate (US, 0);
	seek(US,0,0);	print US @users;
	close(US);
	eval 'flock(US,8);';

# ������ �¸��ڰ� ���� ���� ����
	open(WN,"$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(WN,1);';
	seek(WN,0,0);  @winners = <WN>;  close(WN);
	eval 'flock(WN,8);';

	if(!$winners[0]){
		open(WN,"+<$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
		truncate (WN, 0);
		seek(WN,0,0);	print WN $kakiko;
		close(WN);
	}

}#end record

##### ������ �϶�ǥ��
sub icon_table{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">������ �϶�</font>
<br><br>
<table border=1 cellpadding=5 cellspacing=0>

_EOF_

	for($i=0; $i<$#icon1+1; $i++) {
		if($i % 4 eq 0){
			print "<tr align=center>\n";
		}
		print "<td><img src=\"$imgurl/$icon1[$i].gif\"><br>$icon2[$i]</td>\n";
		if($i % 4 eq 3){
			print "</tr>\n";
		}
	}

	print "</table><br>\n";
	print "<form><input type=\"button\" value=\"  CLOSE  \" onClick=\"top.close();\"></form><br>\n";

	&chosaku;

}#end icon_table

##### ���� ���� ó��
sub user_check{

	$saku = $form{'saku'};
	$pass = $form{'pass'};
	$home = $form{'home'};

	open(US,"$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	$user_jun = 1;
	foreach(@users){
		($checksaku,$checkpass,$d,$checkteam) = split /<p>/;
		if($form{'kanri_mode'}){
			if($form{'team'} eq $checkteam){
				$userdata = $_;
				last;
			}
		}else{
			if($saku eq $checksaku){
				if($pass eq $checkpass){
					$userdata = $_;
					&set_cookie;
					last;
				}else{
					&error('�н����尡 �߸��Ǿ���. ');
				}
			}
		}
		$user_jun++;
	}
	if($userdata eq ''){
		&error('���� �����Ͱ� �߰ߵ��� �ʾҽ��ϴ�. �ű� ����� �ּ���. ');
	}

	return $userdata;

}#end user_check

##### �ڸ�Ʈ ���� ó��
sub comsyori{

	if(length($form{'comtext'}) < 1 || length($form{'comtext'}) > $comleng * 2){ &error('�ڸ�Ʈ�� ���̰� �ùٸ��� �ʾ�. '); }

	open(CF,"+<$commentfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(CF,2);';

	@comments = <CF>;
	if((split(/<>/, $comments[0]))[1] eq $form{'saku'}){ &error('�������� ����� �� �� ����. '); }
	$kakiko = "0<>$form{'saku'}<>$form{'home'}<>$times<>$form{'comtext'}<>$form{'team0'} $form{'ten0'} - $form{'ten1'} $form{'team1'}<>\n";

	unshift(@comments, $kakiko);
	splice(@comments, $com_max);

	truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

}#end comsyori

##### ������ ȭ��
sub kanri{

	if($form{'kanripass'} ne $kanri_pass){ &error('�н����尡 �ٸ��ϴ�. '); }

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">���� ��� ȭ��</font><br>
<br><br><br>
������ �Է��� �ּ���. <br>
<form action=$cgifile method=$method>
<input type=hidden name=login value=1>
<input type=hidden name=kanri_mode value=1>
<input type=text name=team size=15>	<input type=submit name=login value="Enter">
</form>
<br><br>

_EOF_

# �ڸ�Ʈ
	open(CF,"$commentfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	print "<form action=$cgifile method=$method>\n";
	print "<table border=1 width=$ysize cellpadding=5 cellspacing=0>\n";
	print "<tr align=center><td>���� ���� ���� �ڸ�Ʈ</td></tr>\n";

	$i = 0;
	foreach(@comments){
		($no, $saku, $home, $date, $com, $kekka) = split(/<>/, $_);
		$date = &date($date);

		print "<tr><td bgcolor=\"FFFFFF\">\n";
		if($no){
			if($kekka){ $kekka = "�� $kekka ��"; }
			print "<input type=checkbox name=del$i value=$i> ���״��� �� �� $com �� $kekka ($date) \n";
		}else{
			print "<input type=checkbox name=del$i value=$i> $saku �� �� $com �� �� $kekka �� ($date) \n";
		}
		print "</td></tr>\n";

		$i++;
	}
	print "</table><br>\n";
	print "<input type=submit name=comdel value=\"�ڸ�Ʈ ����\">\n";
	print "</form><br><br>\n";

	&chosaku;

}#end kanri

##### �ڸ�Ʈ�� ���� ó��
sub comdelete{

	open(CF,"+<$commentfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(CF,2);';

	@comments = <CF>;

	$i = 0;
	foreach(@comments){
		if($i eq $form{"del$i"}){ $_ = ''; }
		$i++;
	}

	truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

}#end comdelete

##### ������ ��� ǥ��
sub game_log{

	open(LG,"$leaguefold/$logfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(LG,0,0);  @glog = <LG>;  close(LG);

	$g_no = $form{'no'};
	($d, $d, $log_pri) = split(/<>/,@glog[$g_no]);

	&header;

	print "$log_pri<br><br>\n";

	&chosaku;

}#end game_log

##### �� ��Ʈ��
sub team_sort1{

	@tmp1 = ();
	foreach(@users) {
 		my ($saku,$dmy,$dmy,$team,$icon,$dmy,$dmy,$teamdata) = split /<p>/;
		my ($lastjun, $win, $wincon, $winmax, $lose) = split(/<>/, $teamdata);
		$game = $win + $lose;
		push(@tmp1, $game);
	}
	@gameranks = @users[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];

	@tmp2 = @tmp3 = @tmp4 = @else_teams = ();
	foreach(@gameranks){
 		my ($saku,$dmy,$dmy,$team,$icon,$dmy,$dmy,$teamdata) = split /<p>/;
		my ($lastjun, $win, $wincon, $winmax, $lose) = split(/<>/, $teamdata);
		$game = $win + $lose;
		if($game){
			push(@tmp2, $win);
			push(@tmp3, $winmax);
			push(@tmp4, $lose);
		}else{
			push(@else_teams, $_);
		}
	}
	@winranks = @gameranks[sort {$tmp2[$b] <=> $tmp2[$a] || $tmp4[$a] <=> $tmp4[$b] || $tmp3[$b] <=> $tmp3[$a]} 0 .. $#tmp2];

}#end team_sort1

##### �� ����
sub rule{

	&header;

	print <<"_HTML_";
<font color="$tcolor" size="$tsize">��</font>

<hr size="1">
<br>
<table border="1" width="$ysize" cellpadding="5" cellspacing=0 bgcolor="FFFFFF" bordercolor="009900"><tr><td>
<font size="2">
�� ���� ��<BR><BR>
���������� ����� <b>$league_limit �ϰ��� ������</b>�� �ǽ��մϴ�. ���� ���� ������ OK�Դϴ�. <BR><BR>
����������� �� �ִ� ���� �ִ�� <b>$team_max ��</b>�Դϴ�. <br><br>
���������ڴ� <b>����$league_time��</b>�� ����˴ϴ�. <br><br>
������������������ �ִ�<b>$league_game ���ձ���</b>�ǽ��� �� �ֽ��ϴ�. <BR><BR>
��������¥�� $league_limit���� ������, ���� ������ <b>��� �ʱ�ȭ</b> �˴ϴ�. <BR><BR>
���������� <b>$delete_win���̻�</b>�ϰ� ������ �������� �ʱ� ������, �״�δ����� �������� ������ ���� �ֽ��ϴ�. <BR><BR>
�������ٸ�, ���� �Ⱓ�� <b>�ѹ��� ������ �ǽ����� �ʰ� $nogamelimit�� �̻�</b> ����ϸ� �����˴ϴ�(���� ���� �Ĵ� Ư�� ����). <BR><BR>
��������Ͻô� <b>���� $totpoint ����Ʈ</b>�� �ɷ�ġ�� ����� �ּ���. <BR><BR>
�������� ������ ��\��ġ��<b>�հ��$para_min~$para_max</b>�� ���̷� �� �ּ���. <BR><BR>
�������� �ɷ�ġ�� ���� <b>10�� $ten_max��</b>, <b>8~9�� $eight_max��</b>���� �Դϴ�. <BR><BR>
������������ <b>$between�� ����</b> �ǽ��� �� �ֽ��ϴ�. <BR><BR>
���������տ� ����� ��, ������ Ÿ���� ������ �� �ֽ��ϴ�. <br><br>
������������ Ÿ���� ���ؼ���, <b>���� ������ 9</b>, <b>��� ������ 10</b> ���� �� �ּ���. <br><br>
���������� ���� <b>�������� ��</b> �Դϴ�. ���տ� �̱� ���� �״�� �������� ���� �˴ϴ�. <BR><BR>
�������������� ������ <b>����� ����</b> �մϴ�. <br><br>
������������������ <b>$camp_limitȸ����</b>��<b>ķ�� ��</b>���� ����ϴ�. <BR><BR>
������ķ�������� ��Ͻÿ� ����, �� ������ �ɷ�ġ�� ������ �� �ֽ��ϴ�. <BR><BR>
���������� ������ ��ŷ�� �ֽ��ϴ�. ��ŷ ������ ��ǥ�� ��, ���� ������ ����� �ּ����<BR><BR>
�� ������ �帧�� ����<BR><BR>
������������ �帧�� �� ������ ��\���� �������� �����ϴ�. <BR><BR>
�������⺻�� ������ ����, Ÿ�ڰ� ��, Ÿ���� ���� ���� �����δٶ��, ������ �߱��� ����� �����Դϴ�. <BR><BR>
�� ������ ��\�¿� ����<BR><BR>
�������Ŀ���������Ÿ�� ������ �Ǳ� ������, ������ ��������. <BR><BR>
��������Ȯ����������Ÿ�� �� �ǰ�, ��Ÿ�� ������� �����̵ȴ�. <BR><BR>
�������޸��⡤�������״�� �޸���, ���翡 ������ ��ħ, ���񿡵� ����. <BR><BR>
���������񡤡��� ������ ��Ʈ�� ����ϱ� ����. �ܾߴ� ���� �Ǳ� ����. <BR><BR>
�������ӱ�������������. ������ ���ϱ� ������, ������ ��Ÿ�� �Ǳ� ����. ������. <BR><BR>
��������ȭ�������־����°�. ������ ������, ��Ÿ�� �Ǳ� ����. <BR><BR>
������������������Ÿ����������� ����. <BR><BR>
���������¡����������� ��ġ�� ����. <BR><BR>
���������� �ǽġ������������̴ٸ� Ÿ�ڰ� ���� ����, �ƴϸ� ���� ���� ����. <br><br>
��������Ʈ��������Ʈ�� ����(����)����. <br><br>
���������硤�������簡 ����(����)����. <br><br>
������������ �ǽġ����������ɷ´�� �̴°� �ƴϸ� ���������� �����̴°�. <br><br>
��������Ƽ���̼ǡ��������� �Ķ����. �� �̴����� ����Ʈ. �����̳� ��Ÿ������ UP, �����̳� ���������� DOWN. <br><br>
</font>
</td></tr></table>
</form>
<br>

_HTML_

	&footer;
	&chosaku;

}

##### ������ ���
sub date {

	local ($times) = $_[0];
	($dsec,$dmin,$dhour,$dday,$dmon) = localtime($times);
	$dmon++;
	if ($dsec < 10)  { $dsec  = "0$dsec";  }
	if ($dmin < 10)  { $dmin  = "0$dmin";  }
	if ($dhour < 10) { $dhour = "0$dhour"; }
	if ($dday < 10)  { $dday  = "0$dday";  }
	if ($dmon < 10)  { $dmon  = "0$dmon";  }
	$ddate = "$dmon/$dday $dhour:$dmin";

	return $ddate;

}#end date

##### ��Ű�� ����
sub set_cookie{
	$ENV{'TZ'} = "GMT"; # ���� ǥ�ؽø� ���
	local($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg)=localtime(time+30*24*60*60);
	$yearg += 1900;
	if ($secg  < 10)  { $secg  = "0$secg";  }
	if ($ming  < 10)  { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }
	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$ENV{'TZ'} = "Japan";
	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";
	$cook="pass<>$form{'pass'}\,saku<>$form{'saku'}\,home<>$form{'home'}";
	print "Set-Cookie: BASEBALL=$cook; expires=$date_gmt\n";

}#end set_cookie

##### ��Ű�� ���
sub get_cookie{
	@pairs = split(/;/, $ENV{'HTTP_COOKIE'});
	foreach (@pairs) {
		local($key,$val) = split(/=/);
		$key =~ s/\s//g;
		$GET{$key} = $val;
	}
	@pairs = split(/,/, $GET{'BASEBALL'});
	foreach (@pairs) {
		local($key,$val) = split(/<>/);
		$COOK{$key} = $val;
	}
	$c_pass = $COOK{'pass'};
	$c_saku = $COOK{'saku'};
	$c_home = $COOK{'home'};

	if ($in{'pass'}){ $c_pass = $in{'pass'}; }
	if ($in{'saku'}){ $c_saku = $in{'saku'}; }
	if ($in{'home'}){ $c_home = $in{'home'}; }

}#end get_cookie

##### �������� ó��
sub error {

	$err_msg = @_[0];

	&header;

	print <<"_ERROR_";
<html><head><title>ERROR</title></head>
$body
<font color="$tcolor" size="$tsize">����</font>
<br><br><br>
$err_msg<BR>
</body>
</html>
_ERROR_

exit;

}#END error

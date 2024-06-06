#!/usr/bin/perl

#----------------------------------------------------------------------
#	 극공간을 초월하는 리그 2 ver 3.00b (Free)
#	 AUTHOR	: 에
#	 E-MAIL	: osktaka@hotmail.com
#	 URL	: http://homepage2.nifty.com/osktaka/
#
#          한글번역 : jjangg96@hanmail.net
#          한글배포 : http://www.x2-dr.com
#
#	이 스크립트는 프리입니다만, 상용 이용은 금지, 또 재배포는 인정되지 않으므로 주의해 주십시오.
#	스크립트에 관한 질문은"에"에게 부탁합니다.
#	이 스크립트를 사용해 일어나게 되는 문제에 책임은 지지 않습니다.
#	이 스크립트는 아래의 이용 규정에 따라 배포되고 있습니다.
#	http://homepage2.nifty.com/osktaka/down/down_top.htm
#
#	각 파일의 퍼미션은,
#	확장자(extension)가. cgi의 것은 755,. dat의 것은 666,. ini의 것은 644입니다.
#
#----------------------------------------------------------------------


$| = 1;
require './jcode.pl';
require './gekipawa.ini';

########## 로컬 변수 지정
sub kankyou{

$totpoint		= '200';		# 팀의 파라미터 최대치

#### 아이콘 리스트의 취득
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

if($mente){ &error('메인트넌스중입니다. 잠깐 기다려 주세요. '); }

# 등록 처리
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


##### 디코드＆로컬 변수에 주고 받아
sub decode{

#입력된 값을 디코드
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

##### 로그 read
sub readlog{

# 시간의 취득
	
	$times = time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$years = sprintf("%02d",$years + 1900);
	$month = sprintf("%02d",$mon + 1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$sec = sprintf("%02d",$sec);

# 리그전 종료 처리
	open(PR,"$past_rankfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(PR,0,0);  @past_rank = <PR>;  close(PR);
	($pr_date, $pr_dai) = split(/<d>/, $past_rank[0]);

	if(!$past_rank[0]){
		$kakiko_times = $times - ((($hour - $league_time + 24) % 24 ) * 3600 + $min * 60 + $sec);
		$kakiko = "$kakiko_times<d>0<d><d><d><d>\n";
		$league_day = 1;

		open(PR,">>$past_rankfile") || &error('지정된 파일이 열리지 않습니다. ');
			eval 'flock(PR,2);';
			seek(PR,0,0);	print PR $kakiko;
		close(PR);
			eval 'flock(PR,8);';
	}elsif($pr_dai eq -1){
		&error('리그 갱신 처리중입니다. 당분간 기다리고 있어♪');
	}else{
		$league_day = int(($times - $pr_date) / (60 * 60 * 24)) + 1;
	}

	if($league_day > $league_limit){ require './geki_else.cgi'; &league_end; $league_day = 1; }

	$kitei_hit = $league_day * 25;
	$kitei_pit = $league_day * 25;

	$pr_dai++;
	$league_dai = "<font size=4>제<b>$pr_dai</b>회</font>";

}#end readlog

##### 헤더 표시
sub header{

	print "Content-type: text/html\n\n";#컨텐트 타입 출력
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
<!--광고 배너 삽입 위치, 페이지 상부-->

_EOF_

}#end header

##### 풋터 표시
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

##### 저작권 표시
sub chosaku{

	print <<"_CHOSAKU_";
</center>
<hr size="1">
<div align="right"><a href="http://homepage2.nifty.com/osktaka/" target="_blank"><font size="2">극공간을 초월하는 리그 2 ver 3.00b (Free)</font></a></div>
<div align="right"><a href="http://www.x2-dr.com/" target="_blank"><font size="2">X2-DR.com 웹게임 커뮤니티 : 한글판 배포
<div align="right"><a href="http://www.watsescape.com/" target="_blank"><font size="2">아이콘 사용 : 파와 소재
</font></a></div>
<!--광고 배너 삽입 위치, 페이지 하부-->
</body>
</html>
_CHOSAKU_

}#end chosaku

##### 리그 일자 표시
sub top1{

	if($league_day eq 1){
		$l_day_pri = "－<font size=6 color=\"FF0000\"><b> 첫날 </b></font>－";
	}elsif($league_day eq $league_limit){
		$l_day_pri = "－<font size=6 color=\"FF0000\"><b> 마지막 날 </b></font>－";
	}else{
		$l_day_pri = "－<font size=6 color=\"FF0000\"><b> $league_day </b></font><font size=4>일째</font>－";
	}
	$l_day_pri = "$l_day_pri<br>(날은 매일$league_time시로 바뀝니다)";

	print <<"_EOF_";
	<br>
	$league_dai<font size=4> 극공간을 초월하는 리그 2</font><br>
	$l_day_pri<br><br>

_EOF_

	if($bbs_mode){
		print "[ <a href=$bbs_url target=_blank>$bbs_name</a> ]<br><br>\n";
	}

}#end top1

##### 탑 페이지
sub top{

	open(US,"$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
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
		$sinki = "　　<input type=submit name=sinki_make value=\"NEW\">";
	}

# 챔피언
	open(WN,"$leaguefold/$winfile") || &error('지정된 파일이 열리지 않습니다. ');
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
	$champ_pri[2] = "<td><font size=5 color=\"DD9966\"><B>Now Champion! </B></font> (현재<font color=\"FF0000\" size=7><B>$wincon</B></font>연승중!  )<br>\n";
	$champ_pri[3] = "$icon_pri[1] <br>【 감독 : $saku 】$win승 $lose패\n";
	$champ_pri[4] = "<br></td></tr></table>\n";

# 최근의 시합
	open(LG,"$leaguefold/$logfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(LG,0,0);  @glog = <LG>;  close(LG);

	@game_pri = ();
	$game_pri[0] = "<table border=1 width=100% cellspacing=0 cellpadding=5><tr align=center><td>최근 5 시합의 결과</td></tr>\n";

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

# 코멘트
	open(CF,"$commentfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	@com_pri = ();
	$com_pri[0] = "<table border=1 width=\"$ysize\" cellpadding=5 cellspacing=0>\n";
	$com_pri[1] = "<tr align=\"center\"><td>시합 후의 감독 코멘트</td></tr>\n";
	$com_pri[2] = "<tr><td bgcolor=\"FFFFFF\">\n";

	$i = 0;
	foreach(@comments){
		($no, $saku, $home, $date, $com, $kekka) = split /<>/;
		$date = &date($date);
		if($home){ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a> "; }
		if($no){
			if($kekka){ $kekka = "【 $kekka 】"; }
			$com_pri[$i+3] = "■ 리그뉴스 ： 「 $com 」 $kekka ($date) \n";
		}else{
			$com_pri[$i+3] = "□ $saku ： 「 $com 」 【 $kekka 】 ($date) \n";
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

    $c_home =~ s/http:\/\///g;	# 주소의 처리

	print <<"_EOF_";
<table width=$ysize cellpadding=10>
	<tr align=center>
	<td width=75%>
	<font size=5 color="008000"><b>－ 리그 상황 －</b></font><br>
	<table border=1 width="100%" cellspacing=0 cellpadding=5>
		<tr align=center>
		<td><font color="#FF0000" size=5><b>선두</b></font></td>
		<td>
		<table border=0 width=70%>
			<tr align=center>
			<td>$icon_pri[0]
			<font size=3>($saku[0])<br>$win[0]승 $lose[0]패</font>
			</td></tr>
		</table>
		</td></tr>
		<tr align=center>
		<td><font size=4><b>2위</b></font></td>
		<td><font size=4><b>$team[1]</b></font>($saku[1])<br>$win[1]승 $lose[1]패</font>
		</td></tr>
		<tr align=center>
		<td><b>3위</b></td>
		<td><b>$team[2]</b>($saku[2])<br>$win[2]승 $lose[2]패</font>
		</td></tr>
	</table>
	</td>
	<td width=30%>

	<table border=1 width=100% cellspacing=0 cellpadding=5>
		<tr align=center>
		<td>
		<br>$userlimit 일간 시합을 하지 않으면, 유저 데이터는 소거됩니다.<br><br>

		<form action=$cgifile method=$method>
		<table width=170>
			<tr>
			<td width=75>이름</td>
			<td width=95><input type=text name=saku size=15 value=$c_saku></td>
			</tr><tr>
			<td width=75>패스워드</td>
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
<input type=submit name=kanri value="관리용">
</form>

_EOF_

	&chosaku;

}#end top

##### 신규 등록 화면
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
	@position = ('포수','1루수','2루수','3루수','유격수','좌익수','중견수','우익수');
	foreach(@position) {
		push @positlist, "<option value=$_>$_\n";
	}
	if($icon_use)	{ $icon_pri = "<tr><td>아이콘</td><td><select name=\"icon\">@iconlist</select> [ <a href=\"$cgifile?mode=icon_table\" target=\~_blank\">아이콘 일람</a>  ]</td></tr>"; }
	else			{ $icon_pri = ''; }

	&header;
	&java_sum;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">신규 등록</font>

<form action="$cgifile" method="$method">
<input type="submit" value="처음화면으로 돌아온다">
</form>
<br>
<form action="$cgifile" method="$method" name=para>
<table border=1 width=$ysize cellpadding=5>
	<tr>
	<td width=60%>
	<br>
	<table width=100%>
		<tr>
		<td>팀의 이름</td>
		<td><input type=text name=team size=15>(한글,영어<B>$nameleng</B>자까지)</td>
		</tr>
		$icon_pri
		<tr>
		<td>당신의 이름</td>
		<td><input type=text name=saku size=15>(한글,영어<B>$nameleng</B>자까지)</td>
		</tr>
		<tr>
		<td valign=top>타입<br>(1:소 - 10:다)</td>
		<td>
		<table border=1 cellspacing=0>
			<tr align=center>
			<td>공격 의식</td>
			<td>번트</td>
			<td>도루</td>
			<td>데이터 의식</td>
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
		<td>홈 페이지</td>
		<td><input type=text name=home size=30 value="http://"></td>
		</tr>
		<tr>
		<td>패스워드</td>
		<td><input type=password name=pass size=10>(영어,숫자<b>$passleng</b>자까지)</td>
		</tr>
	</table>
	<br>
	</td>
	<td width=40% align=center>

_EOF_

	&parasum_pri;

	print <<"_EOF_";
	<br>
	<input type=submit name=make_end value="등록">
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

##### 능력치 합계 표시
sub parasum_pri{

	print <<"_EOF_";

	☆ 선수능력치의 결정 방법 ☆<br><br>
	<table>
		<tr>
		<td>·각 선수능력치의 합계는</td>
		<td><b>$para_min</b>~<b>$para_max</b></td>
		</tr>
		<tr>
		<td>·팀 전체의 합계는<b>$totpoint</b></td>
		<td><strong>현재：</strong><input type=text value=$totpoint name=para_t size=4></td></tr>
		<tr>
		<td>·파라미터<b>10</b>의 수는<b>$ten_max</b>개</td>
		<td><strong><font color="#FF0000">현재</font>：</strong><input type=text value=0 name=para_10 size=2></td></tr>
		<tr>
		<td>·파라미터<b>8</b>~<b>9</b>의 수는<b>$eight_max</b>개까지</td>
		<td><strong><font color="#0000FF">현재</font>：</strong><input type=text value=0 name=para_89 size=2></td></tr>
	</table>

_EOF_

}#end parasum_pri

##### 능력치 합계 JavaScript
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

##### 선수 등록 테이블
sub make_table{

	print "수비 위치를 선택하고, 이름과 4개의 능력치를 기입해 주세요. \n";
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
			print "<tr align=center><td rowspan=9>타자</td>\n";
			print "<td>타순</td><td>위치</td><td>이름(한글,영어<b>5</b>자까지)</td><td>파워</td><td>정확도</td><td>달리기</td><td>수비력</td><td><b>합계</b></td></tr>\n";
		}elsif($i eq 8){
			print "<tr align=center><td rowspan=3>투수</td>\n";
			print "<td>타순</td><td>위치</td><td>이름</td><td>속구</td><td>변화구</td><td>제구력</td><td>수비력</td><td><b>합계</b></td></tr>\n";
		}
		print "<tr align=center><td>$jun</td>\n";
		if($i < 8){
			print "<td><select name=posit$i>@{$positlist[$i]}</select></td>\n";
		}else{
			print "<td>투수</td>\n";
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

##### 등록 확인 화면
sub make_end{

	$saku		= $form{'saku'};
	$pass		= $form{'pass'};
	$home		= $form{'home'};
	$team		= $form{'team'};
	$icon		= $form{'icon'};

# 이름의 길이 체크
	if((length($team) < 1) || (length($team) > $nameleng *2)){ &error("이름의 길이는$nameleng 자까지 해. "); }
	if((length($saku) < 1) || (length($saku) > $nameleng *2)){ &error("이름의 길이는$nameleng 자까지 해. "); }

# 리모트 호스트 취득
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# 이름＆팀명의 중복 체크
 	open(US,"$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	foreach(@users){
		($checksaku,$checkpass,$d,$checkteam,$d,$d,$checkip) = split /<p>/;
		if($saku eq $checksaku){
			&error('그 유저명은 벌써 사용되고 있습니다. ');
		}
		if($team eq $checkteam){
			&error('그 팀명은 벌써 사용되고 있습니다. ');
		}
		if($host eq $checkip && $double_check){
			&error('팀의 복수 등록은 할 수 없어. ');
		}
	}

	@bosspara	= ($form{'b_act'},$form{'b_bnt'},$form{'b_ste'},$form{'b_mnd'});

	&chara_para;

	&header;

	print <<"_EOF_";
<font color=$tcolor size=$tsize>등록 확인</font>
<br><br>이것으로 등록합니다. 좋습니까? <br>(돌아올 때는 브라우저의 뒤로가기로♪)<br><br>

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

	print "<input type=submit name=login value=\"등록 완료\"></form>\n";

	&touroku_table;
	&chosaku;

}#end make_end

##### 캐릭터마다의 파라미터
sub chara_para{

# 패스워드 체크
	if((length($pass) < 4) || (length($pass) > $passleng)){ &error("패스워드의 길이는 4~$passleng 자까지 해. "); }

#HP의 판정
	($home =~ /^http:\/\/[a-zA-Z0-9]+/) || ($home = '');

	for($i=0; $i<10; $i++){
		$posit[$i]	= $form{"posit$i"};
		$p_name[$i]	= $form{"p_name$i"};
		$para1[$i]	= $form{"para1_$i"};
		$para2[$i]	= $form{"para2_$i"};
		$para3[$i]	= $form{"para3_$i"};
		$para4[$i]	= $form{"para4_$i"};
	}
# 각 캐릭터의 체크
	for($i=0; $i<10; $i++){
		if(length($p_name[$i]) < 1 || length($p_name[$i]) > 5 * 2){ &error('선수의 이름의 길이는 5 자까지 해. '); }
		for($j=0; $j<$i; $j++){
			if($i < 9 && $posit[$i] eq $posit[$j]) { &error('포지션이 중복 되고 있어. '); }
			if($p_name[$i] eq $p_name[$j]){ &error('선수의 이름은 다른 이름으로 해. '); }
		}
	}

# 능력치 체크
	$totalpoint	= 0;
	$check1		= 0;
	$check2		= 0;
	for($i=0; $i<10; $i++){
		if(($para1[$i] < 1 || $para2[$i] < 1 || $para3[$i] < 1 || $para4[$i] < 1) || ($para1[$i] > 10 || $para2[$i] > 10 || $para3[$i] > 10 || $para4[$i] > 10)){
			&error('선수마다의 파라미터는 1~10으로 해. ');
		}
		if(int($para1[$i]) ne $para1[$i] || int($para2[$i]) ne $para2[$i] || int($para3[$i]) ne $para3[$i] || int($para4[$i]) ne $para4[$i]){
			&error('파라미터는 정수로 해. ');
		}
		$totalcheck = $para1[$i] + $para2[$i] + $para3[$i] + $para4[$i];
		if($totalcheck < $para_min || $totalcheck > $para_max){ &error("선수마다의 파라미터의 합계는$para_min~$para_max로 해. "); }
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

	if($check2 > $ten_max)  { &error('파라미터 10의 수가 많아. '); }
	if($check1 > $eight_max){ &error('파라미터 8~9의 수가 많아. '); }
	if($totalpoint ne $totpoint){ &error("파라미터의 합계가$totpoint이 되지 않았어. "); }

}#end chara_para

##### 등록 결과 테이블
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
		<td width=100>팀의 이름</td>
		<td>$team</td>
		</tr>
		<tr>
		<td width=100>당신의 이름</td>
		<td>$saku</td>
		</tr>
		<tr>
		<td valign=top>타입<br>(1:소 - 10:다)</td>
		<td>
		<table border=1 cellspacing=0>
			<tr align=center>
			<td>공격 의식</td>
			<td>번트</td>
			<td>도루</td>
			<td>데이터 의식</td>
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
		<td width=100>홈 페이지</td>
		<td>$home</td>
		</tr>
		<tr>
		<td width=100>패스워드</td>
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
			$condition = "보통";
		}else{
			if($cond[$i] < 2)	{ $condition = "최악"; }
			elsif($cond[$i] < 4){ $condition = "나쁘다"; }
			elsif($cond[$i] < 6){ $condition = "보통"; }
			elsif($cond[$i] < 8){ $condition = "호조"; }
			else				{ $condition = "절호"; }
		}

		if($i eq 0){
			print "<tr align=center><td rowspan=9>타자</td>\n";
			print "<td>순서</td><td>위치</td><td>이름</td><td>상태</td><td>파워</td><td>정확도</td><td>달리기</td><td>수비력</td></tr>\n";
		}elsif($i eq 8){
			print "<tr align=center><td rowspan=3>투수</td>\n";
			print "<td>순서</td><td>위치</td><td>이름</td><td>상태</td><td>속구</td><td>변화구</td><td>제구력</td><td>수비력</td></tr>\n";
		}
		$jun = $i + 1;
		print "<tr align=center><td>$jun</td>\n";
		if($i < 8){
			print "<td>$posit[$i]</td>\n";
		}else{
			print "<td>투수</td>\n";
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

##### 팀 등록 처리
sub record{

# 변수를 옮겨놓는다
	$saku		= $form{'saku'};
	$pass		= $form{'pass'};
	$home		= $form{'home'};
	$team		= $form{'team'};
	$icon		= $form{'icon'};

# 리모트 호스트 취득
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# 로그에 기입하는 스타일의 정형
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
			$players[$i] = "$id<>$jun<>투수<>$p_name<>5<>$para1<>$para2<>$para3<>$para4<>0<>0<>0<>0<>0<>0<>0";
		}
	}
	$players = join('<c>', @players);

	$teamdata  = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0";
	$pointdata = "0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0";
	$bosstype = "$form{'b_act'}<>$form{'b_bnt'}<>$form{'b_ste'}<>$form{'b_mnd'}";
	$kakiko = "$saku<p>$pass<p>$home<p>$team<p>$icon<p>$times<p>$host<p>$teamdata<p>$pointdata<p>$bosstype<p>$players<p><p>0<p>\n";

# 유저 파일에의 기입해
	open(US,"+<$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,2);';

	@users = <US>;
	if($double_check){
		foreach(@users){
			($checksaku,$checkpass,$d,$checkteam,$d,$d,$checkip) = split /<p>/;
			if($host eq $checkip){
				&error('팀의 복수 등록은 할 수 없어. ');
			}
		}
	}
	push(@users,$kakiko);

	truncate (US, 0);
	seek(US,0,0);	print US @users;
	close(US);
	eval 'flock(US,8);';

# 현재의 승리자가 없을 때의 기입
	open(WN,"$leaguefold/$winfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(WN,1);';
	seek(WN,0,0);  @winners = <WN>;  close(WN);
	eval 'flock(WN,8);';

	if(!$winners[0]){
		open(WN,"+<$leaguefold/$winfile") || &error('지정된 파일이 열리지 않습니다. ');
		truncate (WN, 0);
		seek(WN,0,0);	print WN $kakiko;
		close(WN);
	}

}#end record

##### 아이콘 일람표시
sub icon_table{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">아이콘 일람</font>
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

##### 유저 관리 처리
sub user_check{

	$saku = $form{'saku'};
	$pass = $form{'pass'};
	$home = $form{'home'};

	open(US,"$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
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
					&error('패스워드가 잘못되었어. ');
				}
			}
		}
		$user_jun++;
	}
	if($userdata eq ''){
		&error('유저 데이터가 발견되지 않았습니다. 신규 등록해 주세요. ');
	}

	return $userdata;

}#end user_check

##### 코멘트 기입 처리
sub comsyori{

	if(length($form{'comtext'}) < 1 || length($form{'comtext'}) > $comleng * 2){ &error('코멘트의 길이가 올바르지 않아. '); }

	open(CF,"+<$commentfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(CF,2);';

	@comments = <CF>;
	if((split(/<>/, $comments[0]))[1] eq $form{'saku'}){ &error('연속으로 등록은 할 수 없어. '); }
	$kakiko = "0<>$form{'saku'}<>$form{'home'}<>$times<>$form{'comtext'}<>$form{'team0'} $form{'ten0'} - $form{'ten1'} $form{'team1'}<>\n";

	unshift(@comments, $kakiko);
	splice(@comments, $com_max);

	truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

}#end comsyori

##### 관리용 화면
sub kanri{

	if($form{'kanripass'} ne $kanri_pass){ &error('패스워드가 다릅니다. '); }

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">관리 모드 화면</font><br>
<br><br><br>
팀명을 입력해 주세요. <br>
<form action=$cgifile method=$method>
<input type=hidden name=login value=1>
<input type=hidden name=kanri_mode value=1>
<input type=text name=team size=15>	<input type=submit name=login value="Enter">
</form>
<br><br>

_EOF_

# 코멘트
	open(CF,"$commentfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	print "<form action=$cgifile method=$method>\n";
	print "<table border=1 width=$ysize cellpadding=5 cellspacing=0>\n";
	print "<tr align=center><td>시합 후의 감독 코멘트</td></tr>\n";

	$i = 0;
	foreach(@comments){
		($no, $saku, $home, $date, $com, $kekka) = split(/<>/, $_);
		$date = &date($date);

		print "<tr><td bgcolor=\"FFFFFF\">\n";
		if($no){
			if($kekka){ $kekka = "【 $kekka 】"; }
			print "<input type=checkbox name=del$i value=$i> 리그뉴스 ： 「 $com 」 $kekka ($date) \n";
		}else{
			print "<input type=checkbox name=del$i value=$i> $saku ： 「 $com 」 【 $kekka 】 ($date) \n";
		}
		print "</td></tr>\n";

		$i++;
	}
	print "</table><br>\n";
	print "<input type=submit name=comdel value=\"코멘트 삭제\">\n";
	print "</form><br><br>\n";

	&chosaku;

}#end kanri

##### 코멘트의 삭제 처리
sub comdelete{

	open(CF,"+<$commentfile") || &error('지정된 파일이 열리지 않습니다. ');
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

##### 시합의 경과 표시
sub game_log{

	open(LG,"$leaguefold/$logfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(LG,0,0);  @glog = <LG>;  close(LG);

	$g_no = $form{'no'};
	($d, $d, $log_pri) = split(/<>/,@glog[$g_no]);

	&header;

	print "$log_pri<br><br>\n";

	&chosaku;

}#end game_log

##### 팀 소트①
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

##### 룰 설명
sub rule{

	&header;

	print <<"_HTML_";
<font color="$tcolor" size="$tsize">룰</font>

<hr size="1">
<br>
<table border="1" width="$ysize" cellpadding="5" cellspacing=0 bgcolor="FFFFFF" bordercolor="009900"><tr><td>
<font size="2">
□ 놀이 분<BR><BR>
　·　팀을 등록해 <b>$league_limit 일간의 리그전</b>을 실시합니다. 물론 도중 참가도 OK입니다. <BR><BR>
　·　등록할 수 있는 팀은 최대로 <b>$team_max 팀</b>입니다. <br><br>
　·　날자는 <b>매일$league_time시</b>로 변경됩니다. <br><br>
　·　리그전에서는 최대<b>$league_game 시합까지</b>실시할 수 있습니다. <BR><BR>
　·　날짜가 $league_limit일을 지나면, 각종 성적은 <b>모두 초기화</b> 됩니다. <BR><BR>
　·　팀이 <b>$delete_win승이상</b>하고 있으면 없어지지 않기 때문에, 그대로다음의 리그전에 진출할 수가 있습니다. <BR><BR>
　·　다만, 리그 기간중 <b>한번도 시합을 실시하지 않고 $nogamelimit일 이상</b> 경과하면 삭제됩니다(리그 갱신 후는 특히 주의). <BR><BR>
　·　등록시는 <b>팀에 $totpoint 포인트</b>의 능력치를 배분해 주세요. <BR><BR>
　·　각 선수의 능\력치의<b>합계는$para_min~$para_max</b>의 사이로 해 주세요. <BR><BR>
　·　각 능력치의 수는 <b>10이 $ten_max개</b>, <b>8~9가 $eight_max개</b>까지 입니다. <BR><BR>
　·　시합은 <b>$between분 마다</b> 실시할 수 있습니다. <BR><BR>
　·　시합에 등록할 때, 선수의 타순을 변경할 수 있습니다. <br><br>
　·　투수의 타순에 대해서는, <b>선발 투수를 9</b>, <b>대기 투수를 10</b> 으로 해 주세요. <br><br>
　·　대전 상대는 <b>연승중인 팀</b> 입니다. 시합에 이긴 팀이 그대로 연승중의 팀이 됩니다. <BR><BR>
　·　연승중은 투수는 <b>교대로 선발</b> 합니다. <br><br>
　·　리그전에서는 <b>$camp_limit회까지</b>「<b>캠프 인</b>」이 생깁니다. <BR><BR>
　·　캠프에서는 등록시와 같게, 각 선수의 능력치를 변경할 수 있습니다. <BR><BR>
　·　각종 데이터 랭킹이 있습니다. 랭킹 상위를 목표로 해, 여러 선수를 만들어 주세요♪<BR><BR>
□ 시합의 흐름에 대해<BR><BR>
　·　시합의 흐름은 각 선수의 능\력의 판정으로 나갑니다. <BR><BR>
　·　기본은 투수가 던져, 타자가 쳐, 타구에 응해 수비가 움직인다라는, 실제의 야구에 가까운 형태입니다. <BR><BR>
□ 선수의 능\력에 대해<BR><BR>
　·　파워···장타나 포볼이 되기 쉽지만, 삼진이 많아진다. <BR><BR>
　·　정확도···안타가 잘 되고, 장타에 나름대로 도움이된다. <BR><BR>
　·　달리기···말그대로 달리기, 도루에 영향을 끼침, 수비에도 영향. <BR><BR>
　·　수비··· 낮으면 히트를 허락하기 쉽다. 외야는 진루 되기 쉽다. <BR><BR>
　·　속구···빠른공. 삼진을 취하기 쉽지만, 맞으면 장타가 되기 쉽다. 포볼도. <BR><BR>
　·　변화···휘어지는공. 삼진은 적지만, 범타가 되기 쉽다. <BR><BR>
　·　제구···장타에도나름대로 도움. <BR><BR>
　·　상태···찬스나 핀치시 영향. <BR><BR>
　·　공격 의식···공격적이다면 타자가 힘을 발휘, 아니면 수비가 힘을 발휘. <br><br>
　·　번트···번트가 많아(적어)진다. <br><br>
　·　도루···도루가 많아(적어)진다. <br><br>
　·　데이터 의식···선수능력대로 이는가 아니면 직감적으로 움직이는가. <br><br>
　·　모티베이션···은폐 파라미터. 각 이닝으로 리셋트. 득점이나 장타등으로 UP, 실점이나 에러등으로 DOWN. <br><br>
</font>
</td></tr></table>
</form>
<br>

_HTML_

	&footer;
	&chosaku;

}

##### 일자의 취득
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

##### 쿠키의 발행
sub set_cookie{
	$ENV{'TZ'} = "GMT"; # 국제 표준시를 취득
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

##### 쿠키를 취득
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

##### 에러때의 처리
sub error {

	$err_msg = @_[0];

	&header;

	print <<"_ERROR_";
<html><head><title>ERROR</title></head>
$body
<font color="$tcolor" size="$tsize">에러</font>
<br><br><br>
$err_msg<BR>
</body>
</html>
_ERROR_

exit;

}#END error

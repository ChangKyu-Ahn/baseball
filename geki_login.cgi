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


##### 로그인 화면
sub login{

	$userdata = &user_check;

	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata, $gamedata, $campflag) = split(/<p>/, $userdata);
	($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $t_jiseki, $boxsum, $hitsum, $horsum, $stesum, $errsum) = split(/<>/, $teamdata);
	@bosstype = split(/<>/, $bosstype);
	$gamedate = &date($date);

	$game = $win + $lose;
	$game_nokori = $league_game - $game;
	if($game_nokori <= 10){
		if($game_nokori <= 0){ $game_nokori = "시즌 종료"; }
		$game_nokori = "<font size=4 color=\"FF0000\"><b>$game_nokori</b></font>";
	}
	if($icon_use)	{ $icon_pri = "<br><img src=\"$imgurl/$icon\"><br>"; }
	else			{ $icon_pri = ''; }

	if($kaio){
		$winritu  = sprintf("%03d",  ($win    / $game) * 1000);
		$t_dari = sprintf("%03d",  ($hitsum / $boxsum) * 1000);
		$t_ten = sprintf("%0.1f", ($get    / $kaio) * 27);
	}else{
		$winritu  = "000";
		$t_dari = "000";
		$t_ten = "0.0";
	}
	if($kaid){
		$t_bori = sprintf("%0.2f", ($t_jiseki / $kaid) * 27);
	}else{
		$t_bori = "0.00";
	}

	@game_data = split(/<g>/, $gamedata);
	@kekka_pri = ();
	for($i=0; $i<5; $i++){
		($g_time, $kekka, $aite) = split(/<>/, $game_data[$i]);
		$g_time = &date($g_time);
		if($game_data[$i]){
			$kekka_pri[$i] = "<tr align=center><td width=40%>$g_time</td><td width=20%>$kekka</td><td width=40%>$aite</td></tr>\n";
		}else{
			$kekka_pri[$i] = "<tr align=center><td width=40%> - </td><td width=20%> - </td><td width=40%> - </td></tr>\n";
		}
	}

	@players	= split(/<c>/, $charadata);
	@daritu		= ();
	@para = @para_sum = ();
	for($i=0; $i<8; $i++){
		($id[$i], $jun[$i], $posit[$i], $yasyu[$i], $cond[$i], $pow[$i], $mit[$i], $run[$i], $def[$i], $box[$i], $hit[$i], $ten[$i], $hr[$i], $ste[$i] ,$err[$i], $for[$i], $gid[$i]) = split(/<>/, $players[$i]);
		if($box[$i]){
			$daritu[$i] = sprintf("%03d", ($hit[$i] / $box[$i]) * 1000);
			if($daritu[$i] eq 1000){
				$daritu[$i] = "1.000";
			}else{
				$daritu[$i] = ".$daritu[$i]";
			}
		}else{
			$daritu[$i] = ".000";
		}

		$para[$i] = $pow[$i] + $mit[$i] + $run[$i] + $def[$i];
		if($i < 8)	{ $para_sum[0] += $para[$i]; }
		else		{ $para_sum[1] += $para[$i]; }
	}

	@bouritu = ();
	for($i=8; $i<10; $i++){
		($id[$i], $jun[$i], $posit[$i], $pitch[$i], $cond[$i], $fas[$i], $cha[$i], $sei[$i], $def[$i], $pitwin[$i], $pitlose[$i], $kai[$i], $jiseki[$i], $san[$i], $four[$i], $hrp[$i]) = split(/<>/, $players[$i]);
		if($kai[$i]){
			$bouritu[$i] = sprintf("%0.2f", ($jiseki[$i]/ $kai[$i]) * 27);
		}else{
			$bouritu[$i] = "0.00";
		}

		$para[$i] = $fas[$i] + $cha[$i] + $sei[$i] + $def[$i];
		$para_sum[2] += $para[$i];
	}

	@condition = @condition_bar = ();
	for($i=0; $i<10; $i++){
		if($cond[$i] < 2)	{ $condition[$i] = "최악"; $condition_bar[$i] = $cond_bar[0]; }
		elsif($cond[$i] < 4){ $condition[$i] = "나쁜"; $condition_bar[$i] = $cond_bar[1]; }
		elsif($cond[$i] < 6){ $condition[$i] = "보통"; $condition_bar[$i] = $cond_bar[2]; }
		elsif($cond[$i] < 8){ $condition[$i] = "호조"; $condition_bar[$i] = $cond_bar[3]; }
		else				{ $condition[$i] = "절호"; $condition_bar[$i] = $cond_bar[4]; }
		if(!$cond_cha_use)	{ $condition[$i] = ''; }
		if($cond_img_use)	{
			if($cond_cha_use){ $condition[$i] .= "<br>"; }
			$condition[$i] .= "<img src=\"$imgurl/$condition_bar[$i].gif\">";
		}
	}

	@bonuslist = ();
	for($i=0; $i<4; $i++){
		foreach(1..10) {
			if($_ eq $bosstype[$i]){
				push @{$bonuslist[$i]}, "<option value=$_ selected>$_\n";
			}else{
				push @{$bonuslist[$i]}, "<option value=$_>$_\n";
			}
		}
	}

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$title</font>
<BR>

_EOF_

	&top1;

	print <<"_EOF_";
<P>
<form action="$cgifile" method="$method">
<font size=5><b>$team</b> <font size=4><b>리그중</b></font> <font color="FF0000" size=5><b>$user_jun위</b></font></font><br>
[ 최종 시합 일시 - $gamedate ]
<table width="$ysize">
	<tr align="center">
	<td width="35%">
	<table border=1 width="100%" height=100%>
		<tr align=center>
		<td>
		$icon_pri
		감독 ： $saku
		<table width="100%">
			<tr align=center>
			<td colspan=3>타입(1~10)</td>
			</tr>
			<tr align=center>
			<td>수비적</td>
			<td><select name=b_act>@{$bonuslist[0]}</select></td>
			<td>공격적</td>
			</tr>
			<tr align=center>
			<td>번트(소)</td>
			<td><select name=b_bnt>@{$bonuslist[1]}</select></td>
			<td>번트(다)</td>
			</tr>
			<tr align=center>
			<td>도루(소)</td>
			<td><select name=b_ste>@{$bonuslist[2]}</select></td>
			<td>도루(다)</td>
			</tr>
			<tr align=center>
			<td>직감적</td>
			<td><select name=b_mnd>@{$bonuslist[3]}</select></td>
			<td>논리적</td>
			</tr>
		</table>
		</td>
		</tr>
	</table>
	</td>
	<td width="65%">
	<table border=1 width="100%" height="20%">
		<tr align=center>
		<td>시합</td>
		<td>승률</td>
		<td>승리</td>
		<td>패배</td>
		<td>연승</td>
		<td>남은 시합</td>
		</tr>
		<tr align=center>
		<td>$game</td>
		<td>.$winritu</td>
		<td>$win</td>
		<td>$lose</td>
		<td>$winmax</td>
		<td>$game_nokori</td>
		</tr>
	</table>
	<table border=1 width="100%" height="20%">
		<tr align=center>
		<td>타율</td>
		<td>방어율</td>
		<td>득점율</td>
		<td>홈런타</td>
		<td>도루</td>
		<td>실책</td>
		</tr>
		<tr align=center>
		<td>.$t_dari</td>
		<td>$t_bori</td>
		<td>$t_ten</td>
		<td>$horsum</td>
		<td>$stesum</td>
		<td>$errsum</td>
		</tr>
	</table>
	<table border=1 width="100%" height="60%">
		<tr align=center>
		<td colspan=3>최근 5 시합의 결과</td>
		</tr>
		@kekka_pri
	</table>
	</td>
	</tr>
	<tr align=center>
	<td colspan=2>
	<br>
	<table border="1" width="100%">
		<tr align=\"center\">
		<td>　</td><td>　</td><td>이름</td><td>상태</td><td>파워</td><td>정확도</td><td>달리기</td><td>수비</td><td>합계</td><td>타율</td><td>홈런</td><td>타점</td><td>포볼</td><td>희생타</td><td>도루</td><td>실책</td>
		</tr>

_EOF_

	for($i=0; $i<8; $i++){
		@parameta = ($pow[$i],$mit[$i],$run[$i],$def[$i]);
		for($j=0; $j<4; $j++){
			if($parameta[$j] > 7){
				if($parameta[$j] eq 10){
					$parameta[$j] = "<font color=\"FF0000\">$parameta[$j]</font>";
				}else{
					$parameta[$j] = "<font color=\"0000FF\">$parameta[$j]</font>";
				}
			}
		}
		print "<tr align=center><td><input type=text name=jun$i value=$jun[$i] size=1></td>\n";
		print "<td>$posit[$i]</td>\n";
		print "<td>$yasyu[$i]</td>\n";
		print "<td>$condition[$i]</td>\n";
		print "<td><b>$parameta[0]</b></td>\n";
		print "<td><b>$parameta[1]</b></td>\n";
		print "<td><b>$parameta[2]</b></td>\n";
		print "<td><b>$parameta[3]</b></td>\n";
		print "<td>$para[$i]</td>\n";
		print "<td>$daritu[$i]</td>\n";
		print "<td>$hr[$i]</td>\n";
		print "<td>$ten[$i]</td>\n";
		print "<td>$for[$i]</td>\n";
		print "<td>$gid[$i]</td>\n";
		print "<td>$ste[$i]</td>\n";
		print "<td>$err[$i]</td></tr>\n";
	}
	print <<"_EOF_";
	</table>
	<table border="1" width="100%">
		<tr align=\"center\">
		<td>　</td><td>　</td><td>이름</td><td>상태</td><td>속구</td><td>변화</td><td>제구</td><td>수비</td><td>합계</td><td>방어율</td><td>승리</td><td>패배</td><td>탈삼진</td><td>포볼</td><td>피번트</td>
		</tr>

_EOF_

	for($i=8; $i<10; $i++){
		@parameta = ($fas[$i],$cha[$i],$sei[$i],$def[$i]);
		for($j=0; $j<4; $j++){
			if($parameta[$j] > 7){
				if($parameta[$j] eq 10){
					$parameta[$j] = "<font color=\"FF0000\">$parameta[$j]</font>";
				}else{
					$parameta[$j] = "<font color=\"0000FF\">$parameta[$j]</font>";
				}
			}
		}
		print "<tr align=center><td><input type=text name=jun$i value=$jun[$i] size=1></td>\n";
		print "<td>$posit[$i]</td>\n";
		print "<td>$pitch[$i]</td>\n";
		print "<td>$condition[$i]</td>\n";
		print "<td><b>$parameta[0]</b></td>\n";
		print "<td><b>$parameta[1]</b></td>\n";
		print "<td><b>$parameta[2]</b></td>\n";
		print "<td><b>$parameta[3]</b></td>\n";
		print "<td>$para[$i]</td>\n";
		print "<td>$bouritu[$i]</td>\n";
		print "<td>$pitwin[$i]</td>\n";
		print "<td>$pitlose[$i]</td>\n";
		print "<td>$san[$i]</td>\n";
		print "<td>$four[$i]</td>\n";
		print "<td>$hrp[$i]</td>\n";
	}
	print <<"_EOF_";
		</tr>
	</table>
</td>
</tr>
</table>
<br>

_EOF_

	if($form{'kanri_mode'}){
		print "관리 모드 화면입니다. \n";
	}elsif($win + $lose >= $league_game){
		print "한회의 리그는 $league_game 시합까지야. 다음의 리그가 시작될 때까지 기다리고 있어. \n";
	}elsif(($times - $date) < $between * 60 && $win + $lose > 0){
		$nexttimes  = $date + ($between + 1) * 60 - $times;
		$nextminits = int($nexttimes / 60);
		print "다음의 시합까지 $nextminits분 정도 기다리고 있어. \n";
	}else{
		print "<input type=submit name=playkaku value=\"시합 개시\">\n";
		if($campflag < $camp_limit){
			print "　　<input type=submit name=campin value=\"캠프 인\">\n";
		}
		print "\n";
	}

	print <<"_EOF_";
<br><br><br>
<input type=hidden name=saku value="$saku">
<input type=hidden name=pass value="$pass">
<input type=submit name=delekaku value="팀의 삭제">
<br>

_EOF_

	&footer;
	&chosaku;

}#end login

##### 시합 등록 확인
sub playkaku{

	@bosspara	= ($form{'b_act'},$form{'b_bnt'},$form{'b_ste'},$form{'b_mnd'});

# 각 캐릭터의 체크
	for($i=0; $i<10; $i++){
		$dajun[$i] = $form{"jun$i"};
		if($dajun[$i] ne int($dajun[$i])){ &error('타순은 정수로 입력해. '); }
		if($i < 8){
			if($dajun[$i] < 1 || $dajun[$i] > 8){ &error('타자의 타순은 1~8까지 해. '); }
		}else{
			if($dajun[$i] < 9 || $dajun[$i] > 10){ &error('투수의 타순은 9~10까지 해. '); }
		}
		for($j=0; $j<$i; $j++){	if($dajun[$i] eq $dajun[$j]){ &error('타순이 중복 하고 있어. '); } }
	}

	$userdata = &user_check;

	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata) = split(/<p>/, $userdata);
	($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $t_jiseki, $boxsum, $hitsum, $horsum, $runsum, $errsum) = split(/<>/, $teamdata);

	if(($times < $date + $between * 60) && ($win + $lose > 0)){ &error('연속으로 시합은 할 수 없어. '); }

	@players = split(/<c>/, $charadata);
	for($i=0; $i<10; $i++){
		$j = $dajun[$i] - 1;
		($id[$j], $jun[$j], $posit[$j], $p_name[$j], $cond[$j], $para1[$j], $para2[$j], $para3[$j], $para4[$j]) = split(/<>/, $players[$i]);
	}

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">시합 등록 확인</font>
<br><br>이것으로 시합에 도전해도 좋습니까? <br>(돌아올 때는 브라우저의 뒤로가기로♪)<br><br>

<form action="$cgifile" method="$method">

_EOF_

	for($i=0; $i<10; $i++){
		print "<input type=hidden name=jun$i value=$dajun[$i]>\n";
	}
	print "<input type=hidden name=saku value=$saku>\n";
	print "<input type=hidden name=pass value=$pass>\n";
	print "<input type=hidden name=b_act value=$bosspara[0]>\n";
	print "<input type=hidden name=b_bnt value=$bosspara[1]>\n";
	print "<input type=hidden name=b_ste value=$bosspara[2]>\n";
	print "<input type=hidden name=b_mnd value=$bosspara[3]>\n";

	print "<input type=submit name=playball value=\"시합 개시\"></form>\n";

	&touroku_table;
	&chosaku;

}#end playkaku

##### 캠프 화면
sub campin{

	$userdata = &user_check;

	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata, $gamedata, $campflag) = split(/<p>/, $userdata);
	($lastjun, $win, $d, $d, $lose) = split(/<>/, $teamdata);
	@bosstype	= split(/<>/, $bosstype);

	@players	= split(/<c>/, $charadata);
	@positlist	= @parasum = ();
	@positname	= ('포수','1루수','2루수','3루수','유격수','좌익수','중견수','우익수');
	for($i=0; $i<10; $i++){
		($id[$i], $jun[$i], $posit[$i], $p_name[$i], $cond[$i], $para1[$i], $para2[$i], $para3[$i], $para4[$i]) = split(/<>/, $players[$i]);

		for($j=0; $j<8; $j++) {
			$select = '';
			if($positname[$j] eq $posit[$i]){ $select = 'selected'; }
			push @{$positlist[$i]}, "<option value=\"$positname[$j]\" $select> $positname[$j] </option>";
		}
		$parasum[$i] = $para1[$i] + $para2[$i] + $para3[$i] + $para4[$i];
	}
	
	if($icon_use)	{ $icon_pri = "<tr><td>아이콘</td><td><img src=\"$imgurl/$icon\"></td></tr>"; }
	else			{ $icon_pri = ''; }

	if(($win + $lose) eq 0){
		$camp_com = "드디어 새로운 리그의 개막입니다. <br>장기에 걸치는 싸움에 대비해, 전반전에 도전합시다. <br>\n";
	}elsif(($win + $lose) eq int($league_game / 2)){
		$camp_com = "팀 상태를 다시 봐서, 후반전에 도전합시다. <br>\n";
	}else{
		$camp_com = "이쪽은 캠프 모드입니다. <br>팀을 업그레이드해, 리그전 상위를 목표로 합시다. <br>\n";
	}

	$camp_nokori = $camp_limit - $campflag;

	&header;
	&java_sum;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">캠프 인</font>
<br><br>
$camp_com
<br>
캠프 인 나머지 <font size=5 color="#FF0000"><b>$camp_nokori</b></font>회
<form action="$cgifile" method="$method" name=para><br>
<table border=1 width=$ysize cellpadding=5>
	<tr>
	<td width=50%>
	<br>
	<table width=100%>
		$icon_pri
		<tr>
		<td width=100>팀의 이름</td>
		<td>$team</td>
		</tr>
		<tr>
		<td width=100>당신의 이름</td>
		<td>$saku</td>
		</tr>
		<tr>
		<td width=100>홈페이지</td>
		<td>$home</td>
		</tr>
		<tr>
		<td width=100>패스워드</td>
		<td>$pass</td>
		</tr>
	</table>
	<br>
	</td>
	<td width=50% align=center>

_EOF_

	&parasum_pri;

	print <<"_EOF_";
	<br>
	<input type=submit name=camp_end value="등록">
	</td>
	</tr>
</table>
<br>
<br>

_EOF_

	&make_table;

	print <<"_EOF_";
<input type=hidden name=saku value=$saku>
<input type=hidden name=pass value=$pass>
</form>
<br>
<br>

_EOF_

	&chosaku;

}#end campin

##### 캠프 종료 처리
sub camp_rec{

	$userdata = &user_check;
	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata, $gamedata, $campflag) = split(/<p>/, $userdata);

	&chara_para;

# 로그에 기입하는 스타일의 정형
	@players = split(/<c>/, $charadata);
	for($i=0; $i<8; $i++){
		($id, $jun, $posit, $yasyu, $cond, $pow, $mit, $run, $def, $box, $hit, $ten, $hr, $ste, $err, $for, $gid) = split(/<>/, $players[$i]);
		$players[$i] = "$id<>$jun<>$posit[$i]<>$p_name[$i]<>$cond<>$para1[$i]<>$para2[$i]<>$para3[$i]<>$para4[$i]<>$box<>$hit<>$ten<>$hr<>$ste<>$err<>$for<>$gid";
	}
	for($i=8; $i<10; $i++){
		($id, $jun, $posit, $pitch, $cond, $fas, $cha, $sei, $def, $pitwin, $pitlose, $kai, $jiseki, $san, $four, $hrp) = split(/<>/, $players[$i]);
		$players[$i] = "$id<>$jun<>투수<>$p_name[$i]<>$cond<>$para1[$i]<>$para2[$i]<>$para3[$i]<>$para4[$i]<>$pitwin<>$pitlose<>$kai<>$jiseki<>$san<>$four<>$hrp";
	}
	$charadata = join('<c>', @players);

	$campflag++;

# 유저 파일에의 기입해
	open(US,"+<$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,2);';

	@users = <US>;
	foreach(@users){
		($checksaku,$checkpass) = split /<p>/;
		if($checksaku eq $saku && $checkpass eq $pass){
			$_ = "$saku<p>$pass<p>$home<p>$team<p>$icon<p>$date<p>$ip<p>$teamdata<p>$pointdata<p>$bosstype<p>$charadata<p>$gamedata<p>$campflag<p>\n";
			last;
		}
	}

	truncate (US, 0);
	seek(US,0,0);	print US @users;
	close(US);
	eval 'flock(US,8);';

}#end camp_rec

##### 팀의 삭제 확인 화면
sub delekaku{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">팀 데이터의 삭제</font>
<br><br>팀 데이터를 삭제합니다. 좋습니까? <br>(돌아올 때는 브라우저의 뒤로가기로♪)<br><br>

<form action="$cgifile" method="$method">
<input type=hidden name=saku value="$form{'saku'}">
<input type=hidden name=pass value="$form{'pass'}">
<input type=submit name=delete value="삭제한다">
</form>
<br><br>

_EOF_

	&chosaku;

}#end delekaku

##### 팀의 삭제 처리
sub delete{

	open(US,"+<$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,2);';

	@users = <US>;
	foreach(@users){
		($checksaku,$checkpass, $d, $team) = split /<p>/;
		if($checksaku eq $form{'saku'} && $checkpass eq $form{'pass'}){
			$_ = '';
			last;
		}
	}

	truncate (US, 0);
	seek(US,0,0);	print US @users;
	close(US);
	eval 'flock(US,8);';

	open(YD,"+<$leaguefold/$yasyufile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(YD,2);';

	@yasyus = <YD>;
	foreach(@yasyus){
		($checkteam) = split /<>/;
		if($checkteam eq $team){ $_ = ''; }
	}

	truncate (YD, 0); 
	seek(YD,0,0);	print YD @yasyus;
	close(YD);
	eval 'flock(YD,8);';

	open(PD,"+<$leaguefold/$pitchfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(PD,2);';

	@pitchs = <PD>;

	foreach(@pitchs){
		($checkteam) = split /<>/;
		if($checkteam eq $team){ $_ = ''; }
	}

	truncate (PD, 0);
	seek(PD,0,0);	print PD @pitchs;
	close(PD);
	eval 'flock(PD,8);';

}#end delete

1;


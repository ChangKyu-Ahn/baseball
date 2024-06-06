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


##### 랭킹 헤더
sub rank_head{

	@select = ();
	$select[$no] = "selected";
	print <<"_EOF_";
<br>
<form action="$cgifile" method="$method">
<select name=no>
<option value=0 $select[0]>$mesteam_rank
<option value=1 $select[1]>$mesplay_rank
</select>
<input type="submit" name="league_rank" value="표시">
</form>

_EOF_

}#end rank_head

##### 팀 랭킹 출력
sub team_rank{

	open(US,"$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	if($form{'lose'}){
		$rankno = 1;
	}elsif($form{'max'}){
		$rankno = 2;
	}elsif($form{'daritu'}){
		$rankno = 3;
	}elsif($form{'loss'}){
		$rankno = 4;
	}elsif($form{'ten'}){
		$rankno = 5;
	}elsif($form{'hr'}){
		$rankno = 6;
	}elsif($form{'ste'}){
		$rankno = 7;
	}elsif($form{'err'}){
		$rankno = 8;
	}else{
		$rankno = 0;
	}

	&team_sort2;

	@ranking = (@ranking, @else_teams);

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$mesteam_rank</font>
<br><br>

_EOF_

	&rank_head;

	print "－　팀 종합 랭킹(상위 20 팀)　－<BR>\n";
	print "<table border=1 width=$ysize cellspacing=0>\n";
	print "<tr align=\"center\"><td><br></td><td>팀(전리그 순위)</td><td>시합</td><td>승리</td><td>패배</td><td>연승</td><td>승률</td><td>타율</td><td>방어율</td><td>득점율</td><td>홈런</td><td>도루</td><td>실책</td><td>감독</td></tr>\n";
	$ii = 0;
	$select_flag = 0;
	foreach (@ranking) {
 		($saku,$dmy,$home,$team,$icon,$dmy,$dmy,$teamdata) = split /<p>/;
		($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $jiseki, $boxsum, $hitsum, $hrsum, $stesum, $errsum) = split(/<>/, $teamdata);
		$game = $win + $lose;

		$ii++;
		if($ii <= 20){
			if($boxsum){ $daritu  = sprintf("%03d", ($hitsum / $boxsum) * 1000); }
			else{ $daritu = "000"; }
			if($daritu eq 1000){ $daritu = "1.000"; }
			else{ $daritu = ".$daritu"; }
			if($kaio){ $tenritu = sprintf("%.1f", ($get / $kaio) * 27);	}
			else{ $tenritu = "0.0"; }
			if($kaid){ $bouritu = sprintf("%.2f", ($jiseki/$kaid) * 27); }
			else{ $bouritu = "0.00"; }
			if($game){ $winritu = sprintf("%03d", ($win / $game) * 1000); }
			else{ $winritu = "000"; }
			if($winritu eq 1000){ $winritu = "1.000"; }
			else{ $winritu = ".$winritu"; }

			if($game >= $league_game)	{ $game = "<font color=\"FF0000\"><b>$game</b></font>"; }
			if($home)					{ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a>"; }
			if(!$lastjun){
				$lastjun_pri = "(New)";
			}elsif($lastjun < 6){
				$lastjun_pri = "(<b><font color=\"FD57BF\">$lastjun</font></b>)";
			}else{
				$lastjun_pri = "($lastjun)";
			}
			if($wincon){ $team = "<B><font color=\"EE9966\">Now Champion! </font><br><font color=\"669900\">$team</font></B>"; }

			print "<tr align=\"center\"><td>$ii</td><td>$team $lastjun_pri</td><td>$game</td><td>$win</td><td>$lose</td><td>$winmax</td><td>$winritu</td><td>$daritu</td><td>$bouritu</td><td>$tenritu</td><td>$hrsum</td><td>$stesum</td><td>$errsum</td><td>$saku</td></tr>\n";
		}else{
			if($ii eq 21){ print "</table><br><form><select>\n"; $select_flag = 1; }
			print "<option>[$ii] $game 시합 $win승 $lose패 $team\n";
		}
	}
	if($select_flag){ print "</select></form>\n"; }
	else{ print "</table><br>\n"; }

	print <<"_EOF_";

<form action="$cgifile" method="$method">
<input type="hidden" name="league_rank" value=1>
<input type="hidden" name="no" value=$no>
<input type="submit" name="win"  value="승리">
<input type="submit" name="lose" value="패배">
<input type="submit" name="max"  value="연승">
<input type="submit" name="daritu" value="타율">
<input type="submit" name="loss" value="방어율">
<input type="submit" name="ten"  value="득점율">
<input type="submit" name="hr"  value="홈런">
<input type="submit" name="ste" value="도루">
<input type="submit" name="err" value="실책">
</form>

_EOF_

	&footer;
	&chosaku;

}#end team_rank

##### 선수 랭킹
sub play_rank{

# 야수
	open(YD,"$leaguefold/$yasyufile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(YD,1);';
	seek(YD,0,0);  @yasyus = <YD>;  close(YD);
	eval 'flock(YD,8);';

	if($form{'hr'}){
		$rankno = 1;
	}elsif($form{'ten'}){
		$rankno = 2;
	}elsif($form{'ste'}){
		$rankno = 3;
	}elsif($form{'hit'}){
		$rankno = 4;
	}elsif($form{'err'}){
		$rankno = 5;
	}elsif($form{'for'}){
		$rankno = 6;
	}elsif($form{'gid'}){
		$rankno = 7;
	}else{
		$rankno = 0;
	}

	&yasyu_sort1;
	&yasyu_sort2;

# 투수
	open(PD,"$leaguefold/$pitchfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(PD,1);';
	seek(PD,0,0);  @pitchs = <PD>;  close(PD);
	eval 'flock(PD,8);';

	if($form{'pitwin'}){
		$rankno = 1;
	}elsif($form{'pitlose'}){
		$rankno = 2;
	}elsif($form{'p_san'}){
		$rankno = 3;
	}elsif($form{'pitritu'}){
		$rankno = 4;
	}elsif($form{'p_four'}){
		$rankno = 5;
	}elsif($form{'p_hrp'}){
		$rankno = 6;
	}else{
		$rankno = 0;
	}

	&pitch_sort1;
	&pitch_sort2;

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$mesplay_rank</font>
<br><br>

_EOF_

	&rank_head;

	print "－ 타자 －<BR>【규정 타석수：$kitei_hit(일정 * 25)】<br><table border=1 width=\"$ysize\" cellspacing=0>\n";
	print "<tr align=\"center\"><td><br></td><td>선수</td><td>타율</td><td>타석</td><td>타수</td><td>안타</td><td>홈런</td><td>타점</td><td>포볼</td><td>희생타</td><td>도루</td><td>실책</td><td>팀</td></tr>\n";
	$ii = 0;
	foreach (@y_ranking) {
		($y_team,$dmy,$dmy,$dmy,$dmy,$y_yasyu,$dmy,$dmy,$dmy,$dmy,$dmy,$y_box,$y_hit,$y_ten,$y_hr,$y_ste,$y_err,$y_for,$y_gid) = split /<>/;

		$ii++;
		if($ii > 15){ last; }
		if($y_box){
			$daritu = sprintf("%03d", ($y_hit / $y_box) * 1000);
			if($daritu eq 1000){ $daritu = "1.000"; }
			else{ $daritu = ".$daritu"; }
		}
		$daseki = $y_box + $y_for + $y_gid;
		print "<tr align=\"center\"><td>$ii</td><td>$y_yasyu</td><td>$daritu</td><td>$daseki</td><td>$y_box</td><td>$y_hit</td><td>$y_hr</td><td>$y_ten</td><td>$y_for</td><td>$y_gid</td><td>$y_ste</td><td>$y_err</td><td><font size=2>$y_team</font></td></tr>\n";
	}
	print <<"_EOF_";
</table>
<form action="$cgifile" method="$method">
<input type="hidden" name="league_rank" value=1>
<input type="hidden" name="no" value=$no>
<input type="submit" name="daritu" value="타율">
<input type="submit" name="hit" value="안타">
<input type="submit" name="hr"  value="홈런">
<input type="submit" name="ten" value="타점">
<input type="submit" name="for" value="포볼">
<input type="submit" name="gid" value="희생타">
<input type="submit" name="ste" value="도루">
<input type="submit" name="err" value="실책">
</form>

_EOF_

	print "－ 투수 －<BR>【규정 투구 회수：$kitei_pit(일정 * 25)】<br><table border=1 width=\"$ysize\" cellspacing=0>\n";
	print "<tr align=\"center\"><td><br></td><td>선수</td><td>방어율</td><td>승리</td><td>패배</td><td>승률</td><td>투구</td><td>탈삼진</td><td>포볼</td><td>피홈런</td><td>팀</td></tr>\n";
	$ii = 0;
	foreach (@p_ranking) {
 		($p_team,$dmy,$dmy,$dmy,$dmy,$p_pitch,$dmy,$dmy,$dmy,$dmy,$dmy,$p_pitwin,$p_pitlose,$p_kai,$p_jiseki,$p_san,$p_four,$p_hrp) = split /<>/;

		$ii++;
		if($ii > 10){ last; }
		if($p_kai){
			$bouritu = sprintf("%0.2f", ($p_jiseki / $p_kai) * 27);
			$p_winritu = sprintf("%03d", ($p_pitwin / ($p_pitwin + $p_pitlose)) * 1000);
			if($p_winritu eq 1000){ $p_winritu = "1.000"; }
			else{ $p_winritu = ".$p_winritu"; }
			$amari = $p_kai % 3;
			$pitkai = int($p_kai / 3);
		}
		print "<tr align=\"center\"><td>$ii</td><td>$p_pitch</td><td>$bouritu</td><td>$p_pitwin</td><td>$p_pitlose</td><td>$p_winritu</td><td>$pitkai $amari/3</td><td>$p_san</td><td>$p_four</td><td>$p_hrp</td><td><font size=2>$p_team</font></td></tr>\n";
	}
	print <<"_EOF_";
</table>
<form action="$cgifile" method="$method">
<input type="hidden" name="league_rank" value=1>
<input type="hidden" name="no" value=$no>
<input type="submit" name="bouritu" value="방어율">
<input type="submit" name="pitwin" value="승리">
<input type="submit" name="pitlose" value="패배">
<input type="submit" name="pitritu" value="승률">
<input type="submit" name="p_san" value="탈삼진">
<input type="submit" name="p_four" value="포볼">
<input type="submit" name="p_hrp" value="피홈런">
</form>

_EOF_

	&footer;
	&chosaku;

}#end play_rank

##### 팀 획득 포인트 랭킹
sub point_rank{

	open(US,"$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	&team_sort3;

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$mespoint_rank</font>
<br><br><br>
우승：20 p, 2위：15 p, 3위：10 p, 4위：5 p, 5위~10위：1 p, 각 타이틀：5p<br>
<table border=1 width=\"$ysize\" cellspacing=0>
<tr align=\"center\"><td>순서</td><td>팀</td><td>포인트</td><td>우승</td><td>2위</td><td>3위</td><td>수타</td><td>홈런</td><td>타점</td><td>도루</td><td>방어</td><td>최승</td><td>탈삼진</td><td>감독</td></tr>

_EOF_

	$jun = 0;
	$select_flag = 0;
	foreach(@users) {
 		($saku,$dmy,$home,$team,$icon,$dmy,$dmy,$teamdata,$pointdata) = split /<p>/;
		($point, $champ, $secon, $third, $y_dari, $y_hr, $y_ten, $y_ste, $p_bou, $p_win, $p_san) = split(/<>/, $pointdata);

		if(!$point){ last; }
		$jun++;

		if($jun <= 20){
			if($home){ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a>"; }
			print "<tr align=\"center\"><td>$jun</td><td>$team</td><td>$point</td><td>$champ</td><td>$secon</td><td>$third</td><td>$y_dari</td><td>$y_hr</td><td>$y_ten</td><td>$y_ste</td><td>$p_bou</td><td>$p_win</td><td>$p_san</td><td><font size=2>$saku</font></td></tr>\n";
		}else{
			if($jun eq 21){ print "</table><br><form><select>\n"; $select_flag = 1; }
			print "<option>[$jun] $point p $champ-$secon-$third $team\n";
		}
	}
	if($select_flag){ print "</select></form>\n"; }
	else			{ print "</table><br>\n"; }

	&footer;
	&chosaku;

}#end point_rank

##### 과거의 기록 헤더
sub past_head{

	@select = ();
	$select[$form{'no'}] = "selected";
	print <<"_EOF_";
<br>
<form action="$cgifile" method="$method">
<select name=no>
<option value=0 $select[0]>$meslast_kekka
<option value=1 $select[1]>$meslast_team
<option value=2 $select[2]>$meslast_play
<option value=3 $select[3]>$mespast_rank
<option value=4 $select[4]>기록실(1 시합)
<option value=5 $select[5]>기록실(시즌)
</select>
　<input type=submit name=kiroku value="표시">
</form>

_EOF_

}#end past_head

##### 전회 리그 결과
sub last_kekka{

	open(PR,"$past_rankfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(PR,0,0);  @past_rank = <PR>;  close(PR);

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meslast_kekka</font>
<br><br>

_EOF_

	($dmy, $pr_dai, $pr_team, $pr_player) = split (/<d>/, $past_rank[0]);
	($saku,$home,$team,$icon,$game,$win,$winmax,$lose,$winritu,$daritu,$tenritu,$bouritu,$hrsum,$stesum,$errsum) = split(/<>/, $pr_team);

	if($home){ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a>"; }
	if($icon_use){
		if($icon){
			$icon_pri = "<img src=\"$imgurl/$icon\">";
		}else{
			$icon_pri = "NO ICON";
		}
		$icon_pri = "<td><table border=1 cellspacing=0 cellpadding=7 width=100% height=100%><tr align=center><td>$icon_pri</td></tr></table></td>";
		$span = 2;
	}else{
		$icon_pri = '';
		$span = 1;
	}

	&past_head;

	print <<"_EOF_";
<font size=5 color="#FF0000"><b>제$pr_dai회 극공간을 초월하는 리그는 $team가 우승! </b></font>
<br><br><br>

<table width=60%>
	<tr align=center>
	$icon_pri
	<td><br><font size=6><b>$team</b></font><br>
		<font size=3><b>감독：$saku</b></font><br><br>
		<font size=5><b>$game 시합 $win승$lose패</b></font><br><br></td>
	<tr align=center>
	<td colspan=$span>
	<table border=1 cellspacing=0 width=100% style="font-size: 14pt; font-weight: bold">
		<tr align=center>
		<td width=20%>승률</td><td width=30%>$winritu</td><td width=20%>최다 연승</td><td width=30%>$winmax</td>
		</tr>
		<tr align=center>
		<td width=20%>타율</td><td width=30%>$daritu</td><td width=20%>방어율</td><td width=30%>$bouritu</td>
		</tr>
		<tr align=center>
		<td width=20%>득점율</td><td width=30%>$tenritu</td><td width=20%>홈런타</td><td width=30%>$hrsum</td>
		</tr>
		<tr align=center>
		<td width=20%>도루</td><td width=30%>$stesum</td><td width=20%>실책</td><td width=30%>$errsum</td>
		</tr>
	</table>
	</td>
	</tr>
</table>
<br><br><br>

_EOF_

	print"<table width=80%>\n";

	for($i=0; $i<4; $i++){
		if($i eq 0)		{ @rankcom = ('수위타자', '최우수 방어율'); }
		elsif($i eq 1)	{ @rankcom = ('홈런타왕', '최다 승리'); }
		elsif($i eq 2)	{ @rankcom = ('타점왕', '최다 패전'); }
		elsif($i eq 3)	{ @rankcom = ('도루왕', '최다탈삼진'); }

		print "<tr align=center>\n";

		for($j=0; $j<2; $j++){
			print "<td colspan=2 width=50%><br><b>【 $rankcom[$j] 】</b></td>\n";
		}
		print "</tr><tr align=center valign=top>\n";

		for($j=0; $j<2; $j++){
			$k = $i + 4 * $j;
			($seiseki, $p_name, $team, $icon) = split(/<>/, (split(/<c>/, $pr_player))[$k]);
			if(!$seiseki){
				$seiseki = "-"; $p_name = "-"; $team = "-";
			}elsif($i eq 0 && $j eq 0){
				$seiseki = ".$seiseki";
			}
			if($icon_use){
				if($icon){
					$icon_pri = "<img src=\"$imgurl/$icon\">";
				}else{
					$icon_pri = "NO ICON";
				}
				$icon_pri = "<table border=1 cellspacing=0 cellpadding=7><tr><td>$icon_pri</td></tr></table>";
				$align = 'left';
			}else{
				$icon_pri = '';
				$align = 'center';
			}
			print "<td>$icon_pri</td>\n";
			print "<td align=$align><table>\n";
			print "<tr><td>성적</td><td><b>$seiseki</b></td></tr>\n";
			print "<tr><td>이름</td><td><b>$p_name</b></td></tr>\n";
			print "<tr><td>팀</td><td><b>$team</b></td></tr></table></td>\n";
		}
		print "</tr>\n";
	}
	print "</table><br><br>\n";

	&footer;
	&chosaku;

}#end last_kekka

##### 전회 팀 랭킹
sub last_team{

	open(PT,"$leaguefold/$last_teamfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(PT,0,0);  @last_teams = <PT>;  close(PT);

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meslast_team</font>
<br><br>

_EOF_

	&past_head;

	print "<table border=1 width=$ysize cellspacing=0>\n";
	print "<tr align=\"center\"><td>순서</td><td>팀</td><td>시합</td><td>승리</td><td>패배</td><td>연승</td><td>승률</td><td>타율</td><td>방어율</td><td>득점율</td><td>홈런</td><td>도루</td><td>실책</td><td>감독</td></tr>\n";

	$jun = 0;
	$select_flag = 0;
	foreach(@last_teams){
		($saku,$home,$team,$icon,$game,$win,$winmax,$lose,$winritu,$daritu,$tenritu,$bouritu,$hrsum,$stesum,$errsum) = split /<>/;

		$jun++;
		if($jun <= 50){
			$jun_pri = $jun;
			if($jun eq 1){
				$jun_pri = "<font color=\"FF0000\"><b>우승</b></font>";
			}
			if($home){
				$saku = "<a href=\"$home\" target=\"_blank\">$saku</a>";
			}
			print "<tr align=\"center\"><td>$jun_pri</td><td>$team</td><td>$game</td><td>$win</td><td>$lose</td><td>$winmax</td><td>$winritu</td><td>$daritu</td><td>$bouritu</td><td>$tenritu</td><td>$hrsum</td><td>$stesum</td><td>$errsum</td><td><font size=2>$saku</font></td></tr>\n";
		}else{
			if($jun eq 51){
				print "</table><br><form><select>\n";
				$select_flag = 1;
			}
			print "<option>[$jun] $game 시합 $win승 $lose패 $team\n";
		}
	}

	if($select_flag){ print "</select></form><br>\n"; }
	else{ print "</table><br><br>\n"; }

	&footer;
	&chosaku;

}#end last_team

##### 전회 선수 랭킹
sub last_play{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meslast_play</font>
<br><br>

_EOF_

	open(LY,"$leaguefold/$last_yasyufile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(LY,0,0);  @{$last_player[0]} = <LY>;  close(LY);

	open(LP,"$leaguefold/$last_pitchfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(LP,0,0);  @{$last_player[1]} = <LP>;  close(LP);

	&past_head;

	print "<table width=\"$ysize\">\n";

	for($j=0; $j<4; $j++){
		if($j eq 0)		{ @rankcom = ('타율', '방어율');	@ranktop = ('타율', '방어율'); }
		elsif($j eq 1)	{ @rankcom = ('홈런타', '승리');	@ranktop = ('홈런타', '승리'); }
		elsif($j eq 2)	{ @rankcom = ('타점', '패전');	@ranktop = ('타점', '패전'); }
		elsif($j eq 3)	{ @rankcom = ('도루', '탈삼진');	@ranktop = ('도루', '탈삼진'); }

		print "<tr align=center>\n";
		for($i=0; $i<2; $i++){
			print "<td width=50%><br>【 $rankcom[$i] 】<table border=1 width=90% cellspacing=0>\n";
			print "<tr align=center><td>순서</td><td>$ranktop[$i]</td><td>선수</td><td>팀</td></tr>\n";

			@ranking = split(/<d>/, $last_player[$i][$j]);
			$jun = 0;
			foreach(@ranking){
				$jun++;
				($seiseki, $yasyu, $team) = split /<>/;
				if(!$seiseki){
					$seiseki = "-"; $yasyu = "-"; $team = "-";
				}elsif($i eq 0 && $j eq 0){
					$seiseki = ".$seiseki";
				}
				print "<tr align=center><td>$jun</td><td>$seiseki</td><td>$yasyu</td><td>$team</td></tr>\n";
				if($jun eq 10){ last; }
			}
			print "</table></td>\n";
		}
		print "</tr>\n";
	}
	print"</table><br><br>\n";

	&footer;
	&chosaku;

}#end last_play

##### 역대 랭킹
sub past_rank{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$mespast_rank</font>
<br><br>

_EOF_

	&past_head;

	open(PR,"$past_rankfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(PR,0,0);  @past_rank = <PR>;  close(PR);

	print "【 역대 우승 팀 】<BR><table border=1 width=90% cellspacing=0>\n";
	print "<tr align=\"center\"><td>대</td><td>팀</td><td>시합</td><td>승리</td><td>패배</td><td>연승</td><td>승률</td><td>타율</td><td>방어율</td><td>득점율</td><td>홈런</td><td>도루</td><td>실책</td><td>감독</td></tr>\n";

	@play_rank = ();
	for($i=0; $i<$#past_rank; $i++){
		($dmy, $pr_dai, $pr_team, $pr_player) = split (/<d>/, $past_rank[$i]);
		($saku,$home,$team,$icon,$game,$win,$winmax,$lose,$winritu,$daritu,$tenritu,$bouritu,$hrsum,$stesum,$errsum) = split(/<>/, $pr_team);

		if($home){ $saku = "<a href=\"$home\" target=\"_blank\">$saku</a> "; }
		print "<tr align=\"center\"><td>$pr_dai</td><td>$team</td><td>$game</td><td>$win</td><td>$lose</td><td>$winmax</td><td>$winritu</td><td>$daritu</td><td>$bouritu</td><td>$tenritu</td><td>$hrsum</td><td>$stesum</td><td>$errsum</td><td><font size=2>$saku</font></td></tr>\n";

		for($j=0; $j<2; $j++){
			for($k=0; $k<4; $k++){
				($seiseki, $play, $team) = split(/<>/, (split(/<c>/, $pr_player))[$k+4*$j]);
				if($seiseki eq ''){
					$seiseki = $play = $team = "-";
				}elsif($j eq 0 && $k eq 0){
					$seiseki = ".$seiseki";
				}
				$play_rank[$j][$k][$i] = "<tr align=center><td>$pr_dai</td><td>$seiseki</td><td>$play</td><td>$team</td></tr>\n";
			}
		}
	}
	print "</table>\n";
	print "<br><table width=\"$ysize\">\n";

	for($i=0; $i<4; $i++){
		if($i eq 0){	@rankcom = ('수위타자',	'최우수 방어율') ;@ranktop = ('타율',	'방어율'); }
		elsif($i eq 1){ @rankcom = ('홈런타왕',	'최다 승리');	@ranktop = ('홈런타', '승리'); }
		elsif($i eq 2){ @rankcom = ('타점왕',	'최다 패전');	@ranktop = ('타점',	'지고'); }
		elsif($i eq 3){ @rankcom = ('도루왕',	'최다탈삼진');	@ranktop = ('도루',	'탈삼진'); }

		print "<tr align=center>\n";
		for($j=0; $j<2; $j++){
			print "<td><br><br>【 $rankcom[$j] 】<br><table border=1 width=90% cellspacing=0>\n";
			print "<tr align=center><td>대</td><td>$ranktop[$j]</td><td>선수</td><td>팀</td></tr>\n";
			print "@{$play_rank[$j][$i]}";
			print "</table></td>\n";
		}
		print "</tr>\n";
	}
	print "</table><br><br>\n";

	&footer;
	&chosaku;

}#end past_rank

##### 기록실표시
sub each_reco{

	open(RC,"$leaguefold/$recordfile") || &error('지정된 파일이 열리지 않습니다. ');
	seek(RC,0,0);  @records = <RC>;  close(RC);

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meseach_reco</font>
<br><br>

_EOF_

	&past_head;

	@tuika1 = ('1 시합', '시즌');

	if($no eq 4){ &game_rec; }
	else{ &season_rec; }

	&footer;
	&chosaku;

}#end each_reco

##### 1 시합 기록
sub game_rec{

	@table_name	= ('양팀 기록', '팀 기록', '야수 기록', '투수 기록');
	@{$bumon[0]} = ('최장 시합', '최다 득점', '최다 안타', '최다 홈런타', '최다 도루', '최다 삼진', '최다 포볼/데드볼', '최다 실책');
	@{$bumon[1]} = ('최다 득점', '최다 안타', '최다 홈런타', '최다 도루', '최다 삼진', '최다 실책');
	@{$bumon[2]} = ('최다 안타', '최다 홈런타', '최다 타점', '최다 도루', '최다 삼진', '최다 실책');
	@{$bumon[3]} = ('완전 시합', '무안타 무득점 시합', '최다탈삼진', '최다 실점', '최다피홈런타', '최다여포볼/데드볼');
	for($i=0; $i<$#table_name+1; $i++){
		if($i < 2){ @table_top = ('팀', '감독'); }
		else{ @table_top = ('이름', '팀'); }
		print "【 $tuika1[0]$table_name[$i] 】<table border=1 width=$ysize cellspacing=0>\n";
		print "<tr align=center><td>기록명</td><td>기록</td><td>$table_top[0]</td><td>$table_top[1]</td><td>대</td><td>일시</td></tr>\n";

		@kiroku = split(/<d>/, $records[$i]);
		for($j=0; $j<$#{$bumon[$i]}+1; $j++){
			($seiseki, $name1, $name2, $dai, $date) = split(/<>/, $kiroku[$j]);
			$date = &date($date);
			if($seiseki eq ''){
				$seiseki = $name1 = $name2 = $dai = $date = "-";
			}
			print "<tr><td>$bumon[$i][$j]</td><td align=right>$seiseki</td><td align=center>$name1</td><td align=center>$name2</td><td align=center>$dai</td><td align=center>$date</td></tr>\n";
		}
		print "</table><br>\n";
	}

}#end game_rec

##### 시즌 기록
sub season_rec{

	@table_name	= ('팀 기록', '야수 기록', '투수 기록');
	@{$bumon[0]} = ('최다 승리', '최다 패전', '최다 연승', '최고 타율', '최우수 방어율', '최고 득점율', '최다 홈런타', '최다 도루', '최다 실책');
	@{$bumon[1]} = ('최고 타율', '최다 홈런타', '최다 타점', '최다 도루', '최다 안타', '최다 실책');
	@{$bumon[2]} = ('최우수 방어율', '최다 승리', '최다 패전', '최다탈삼진', '최고 승률', '최다 포볼/데드볼', '최다피홈런타');
	@{$jun[0]}	= (0,1,2,3,4,5,6,7,8);
	@{$jun[1]}	= (0,1,2,4,3,5);
	@{$jun[2]}	= (0,1,4,3,2,5,6);
	for($i=0; $i<$#table_name+1; $i++){
		if($i < 1){ @table_top = ('팀', '감독'); }
		else{ @table_top = ('이름', '팀'); }
		print "【 $tuika1[1]$table_name[$i] 】<table border=1 width=$ysize cellspacing=0>\n";
		print "<tr align=center><td>기록명</td><td>기록</td><td>$table_top[0]</td><td>$table_top[1]</td><td>대</td></tr>\n";

		@kiroku = split(/<d>/, $records[$i+4]);
		for($j=0; $j<$#{$bumon[$i]}+1; $j++){
			$k = $jun[$i][$j];
			($seiseki, $name1, $name2, $dai) = split(/<>/, $kiroku[$k]);
			if($seiseki eq ''){
				$seiseki = $name1 = $name2 = $dai = "-";
			}elsif(($i eq 0 && $k eq 3) || ($i eq 1 && $k eq 0) || ($i eq 2 && $k eq 4)){
				$seiseki = ".$seiseki";
			}
			print "<tr><td>$bumon[$i][$k]</td><td align=right>$seiseki</td><td align=center>$name1</td><td align=center>$name2</td><td align=center>$dai</td></tr>\n";
		}
		print "</table><br>\n";
	}

}#end season_rec

##### 팀 소트②
sub team_sort2{

	&team_sort1;

	@tmp5 = ();
	foreach(@winranks) {
 		my ($saku,$dmy,$dmy,$team,$icon,$dmy,$dmy,$teamdata) = split /<p>/;
		my ($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $jiseki, $boxsum, $hitsum, $hrsum, $stesum, $errsum) = split(/<>/, $teamdata);

		if($rankno eq 1){
			$seiseki = $lose;
		}elsif($rankno eq 2){
			$seiseki = $winmax;
		}elsif($rankno eq 3){
			if($boxsum){ $seiseki = sprintf("%03d", ($hitsum / $boxsum) * 1000); }
			else{ $seiseki = 0; }
		}elsif($rankno eq 4){
			if($kaid){ $seiseki = sprintf("%.2f", ($jiseki/$kaid) * 27); }
			else{ $seiseki = 0; }
		}elsif($rankno eq 5){
			if($kaio){ $seiseki = sprintf("%.1f", ($get/$kaio) * 27); }
			else{ $seiseki = 0; }
		}elsif($rankno eq 6){
			$seiseki = $hrsum;
		}elsif($rankno eq 7){
			$seiseki = $stesum;
		}elsif($rankno eq 8){
			$seiseki = $errsum;
		}else{
			last;
		}
		push(@tmp5, $seiseki);
	}

	if($rankno eq 0){
		@ranking = @winranks;
	}elsif($rankno eq 4){
		@ranking = @winranks[sort {$tmp5[$a] <=> $tmp5[$b]}  0 .. $#tmp5];
	}else{
		@ranking = @winranks[sort {$tmp5[$b] <=> $tmp5[$a]}  0 .. $#tmp5];
	}

}#team_sort2

##### 팀 소트③
sub team_sort3{

	@tmp1 = @tmp2 = @tmp3 = @tmp4 = ();
	foreach(@users) {
 		my ($saku,$dmy,$dmy,$team,$icon,$dmy,$dmy,$teamdata, $pointdata) = split /<p>/;
		my ($point, $champ, $secon, $third, $y_dari, $y_hr, $y_ten, $y_ste, $p_bou, $p_win, $p_san) = split(/<>/, $pointdata);
		push(@tmp1, $point);
		push(@tmp2, $champ);
		push(@tmp3, $secon);
		push(@tmp4, $third);
	}
	@users = @users[sort {$tmp1[$b] <=> $tmp1[$a] || $tmp2[$b] <=> $tmp2[$a] || $tmp3[$b] <=> $tmp3[$a] || $tmp4[$b] <=> $tmp4[$a]} 0 .. $#tmp1];

}#end team_sort3

##### 야수 소트 처리 준비
sub yasyu_sort1{

	@boxranks = @tmp1 = ();
	foreach(@yasyus){
 		my ($team,$dmy,$dmy,$dmy,$dmy,$yasyu,$dmy,$dmy,$dmy,$dmy,$dmy,$box,$hit,$ten,$hr,$ste,$err,$for,$gid) = split /<>/;
		$daseki = $box + $for + $gid;
		if($daseki){
			push(@boxranks, $_);
			push(@tmp1, $daseki);
		}
	}
	@boxranks = @boxranks[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];

}#end yasyu_sort1

##### 야수 소트 처리
sub yasyu_sort2{

	@kiteiranks = ();
	@tmp2 = @tmp3 = ();
	foreach(@boxranks) {
 		my ($team,$dmy,$dmy,$dmy,$dmy,$yasyu,$dmy,$dmy,$dmy,$dmy,$dmy,$box,$hit,$ten,$hr,$ste,$err,$for,$gid) = split /<>/;

		$daseki = $box + $for + $gid;
		$daritu = sprintf("%03d", ($hit / $box) * 1000);
		if($rankno eq 0){
			if($daseki >= $kitei_hit){
				$seiseki = $daritu;
				push(@kiteiranks, $_);
				push(@tmp2, $seiseki);
				push(@tmp3, $hit);
			}else{
				last;
			}
		}else{
			if($rankno eq 1){ $seiseki = $hr; }
			elsif($rankno eq 2){ $seiseki = $ten; }
			elsif($rankno eq 3){ $seiseki = $ste; }
			elsif($rankno eq 4){ $seiseki = $hit; }
			elsif($rankno eq 5){ $seiseki = $err; }
			elsif($rankno eq 6){ $seiseki = $for; }
			elsif($rankno eq 7){ $seiseki = $gid; }
			push(@tmp2, $seiseki);
			push(@tmp3, $daritu);
		}
	}

	if($rankno eq 0){
		@y_ranking = @kiteiranks[sort {$tmp2[$b] <=> $tmp2[$a] || $tmp3[$b] <=> $tmp3[$a]} 0 .. $#tmp2];
	}else{
		@y_ranking = @boxranks[sort {$tmp2[$b] <=> $tmp2[$a] || $tmp3[$b] <=> $tmp3[$a]} 0 .. $#tmp2];
	}

}#end yasyu_sort2

##### 투수 소트 처리 준비
sub pitch_sort1{

	@kairanks = @tmp1 = ();
	foreach(@pitchs){
 		my ($team,$dmy,$dmy,$dmy,$dmy,$pitch,$dmy,$dmy,$dmy,$dmy,$dmy,$pitwin,$pitlose,$kai) = split /<>/;
		if($kai){
			push(@kairanks, $_);
			push(@tmp1, $kai);
		}
	}
	@kairanks = @kairanks[sort {$tmp1[$b] <=> $tmp1[$a]} 0 .. $#tmp1];

}#end pitch_sort1

##### 투수 소트 처리
sub pitch_sort2{

	@kiteiranks = ();
	@tmp2 = @tmp3 = ();
	foreach(@kairanks) {
 		my ($team,$dmy,$dmy,$dmy,$dmy,$pitch,$dmy,$dmy,$dmy,$dmy,$dmy,$pitwin,$pitlose,$kai,$jiseki,$san,$four,$hrp) = split /<>/;

		if($rankno eq 0 || $rankno eq 4){
			if($kai >= $kitei_pit * 3){
				$boritu = sprintf("%0.2f", ($jiseki / $kai) * 27);
				if($rankno eq 0){
					$seiseki = $boritu;
					$second = $pitwin;
				}elsif($rankno eq 4){
					$seiseki = sprintf("%03d", ($pitwin / ($pitwin + $pitlose)) * 1000);
					$second = $boritu;
				}
				push(@kiteiranks, $_);
				push(@tmp2, $seiseki);
				push(@tmp3, $second);
			}else{
				last;
			}
		}else{
			if($rankno eq 1){ $seiseki = $pitwin; }
			elsif($rankno eq 2){ $seiseki = $pitlose; }
			elsif($rankno eq 3){ $seiseki = $san; }
			elsif($rankno eq 5){ $seiseki = $four; }
			elsif($rankno eq 6){ $seiseki = $hrp; }
			$boritu = sprintf("%0.2f", ($jiseki / $kai) * 27);
			push(@tmp2, $seiseki);
			push(@tmp3, $boritu);
		}
	}

	if($rankno eq 0){
		@p_ranking = @kiteiranks[sort {$tmp2[$a] <=> $tmp2[$b] || $tmp3[$b] <=> $tmp3[$a]} 0 .. $#tmp2];
	}elsif($rankno eq 4){
		@p_ranking = @kiteiranks[sort {$tmp2[$b] <=> $tmp2[$a] || $tmp3[$a] <=> $tmp3[$b]} 0 .. $#tmp2];
	}else{
		@p_ranking = @kairanks[sort {$tmp2[$b] <=> $tmp2[$a] || $tmp3[$a] <=> $tmp3[$b]} 0 .. $#tmp2];
	}

}#end pitch_sort2

##### 리그 기간 종료 처리
sub league_end{

# 역대 랭킹 파일 일시 기입
	$pr_dai++;
	$kakiko_times = $times - ((($hour - $league_time + 24) % 24 ) * 3600 + $min * 60 + $sec);
	$kakiko = "$kakiko_times<d>-1<d><d><d>\n";
	splice(@past_rank,0,0,$kakiko);

	open(PR,"+<$past_rankfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(PR,2);';
	truncate (PR, 0);
	seek(PR,0,0);	print PR @past_rank;
	close(PR);
	eval 'flock(PR,8);';

	$league_day = $league_limit;

	$kitei_hit = $league_day * 25;
	$kitei_pit = $league_day * 25;

	@rank_top = ();

# 야수 파일 초기화
	open(YD,"+<$leaguefold/$yasyufile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(YD,2);';

	@yasyus = <YD>;
	&yasyu_sort1;

	@lead_player = ();
	@last_yasyu = ();
	@y_title	= ();
	for($i=0; $i<6; $i++){
		$rankno = $i;
		&yasyu_sort2;

		@yasyu_rank = ();
		for($j=0; $j<10; $j++){
			$seiseki = '';
			($team,$dmy,$dmy,$dmy,$dmy,$yasyu,$dmy,$dmy,$dmy,$dmy,$dmy,$box,$hit,$ten,$hr,$ste,$err,$for,$gid) = split(/<>/, $y_ranking[$j]);
			if($i eq 0 && $box)	  { $seiseki = sprintf("%03d", ($hit / $box) * 1000); }
			elsif($i eq 1){ $seiseki = $hr; }
			elsif($i eq 2){ $seiseki = $ten; }
			elsif($i eq 3){ $seiseki = $ste; }
			elsif($i eq 4){ $seiseki = $hit; }
			elsif($i eq 5){ $seiseki = $err; }

			$yasyu_rank[$j] = "$seiseki<>$yasyu<>$team";

			if($j eq 0){
				$lead_player[$i] = $yasyu_rank[0];
				$y_title[$i] = $team;
				$rank_top[1][$i] = "$seiseki<>$yasyu<>$team<>$pr_dai";
			}
		}
		if($i < 4){
			$last_yasyu = join('<d>', @yasyu_rank);
			$last_yasyu[$i] = "$last_yasyu<d>\n";
		}
	}

	splice(@yasyus);

	truncate (YD, 0);
	seek(YD,0,0);	print YD @yasyus;
	close(YD);
	eval 'flock(YD,8);';

	open(LY,"+<$leaguefold/$last_yasyufile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(LY,2);';
	truncate (LY, 0);
	seek(LY,0,0);	print LY @last_yasyu;
	close(LY);
	eval 'flock(LY,8);';

# 투수 파일 초기화
	open(PD,"+<$leaguefold/$pitchfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(PD,2);';

	@pitchs = <PD>;
	&pitch_sort1;

	@last_pitch = ();
	@p_title	= ();
	for($i=0; $i<7; $i++){
		$rankno = $i;
		&pitch_sort2;

		@pitch_rank = ();
		for($j=0; $j<10; $j++){
			$seiseki = '';
	 		($team,$dmy,$dmy,$dmy,$dmy,$pitch,$dmy,$dmy,$dmy,$dmy,$dmy,$pitwin,$pitlose,$kai,$jiseki,$san,$four,$hrp) = split(/<>/, $p_ranking[$j]);
			if($i eq 0 && $kai){ $seiseki = sprintf("%0.2f", ($jiseki / $kai) * 27); }
			elsif($i eq 1){ $seiseki = $pitwin; }
			elsif($i eq 2){ $seiseki = $pitlose; }
			elsif($i eq 3){ $seiseki = $san; }
			elsif($i eq 4 && $pitwin){ $seiseki = sprintf("%03d", ($pitwin / ($pitwin + $pitlose)) * 1000); }
			elsif($i eq 5){ $seiseki = $four; }
			elsif($i eq 6){ $seiseki = $hrp; }

			$pitch_rank[$j] = "$seiseki<>$pitch<>$team";

			if($j eq 0){
				$lead_player[$i+4] = $pitch_rank[0];
				$p_title[$i] = $team;
				$rank_top[2][$i] = "$seiseki<>$pitch<>$team<>$pr_dai";
			}
		}
		if($i < 4){
			$last_pitch = join('<d>', @pitch_rank);
			$last_pitch[$i] = "$last_pitch<d>\n";
		}
	}
	splice(@pitchs);

	truncate (PD, 0);
	seek(PD,0,0);	print PD @pitchs;
	close(PD);
	eval 'flock(PD,8);';

	open(LP,"+<$leaguefold/$last_pitchfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(LP,2);';
	truncate (LP, 0);
	seek(LP,0,0);	print LP @last_pitch;
	close(LP);
	eval 'flock(LP,8);';

# 유저 파일 초기화
	open(US,"+<$leaguefold/$userfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(US,2);';

	@users = <US>;

	for($i=0; $i<9; $i++){
		$rankno = $i;
		&team_sort2;

 		($saku,$pass,$home,$team,$icon,$date,$ip,$teamdata) = split(/<p>/, $ranking[0]);
		($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $jiseki, $boxsum, $hitsum, $hrsum, $stesum, $errsum) = split(/<>/, $teamdata);
		if($i eq 0){
			$seiseki = $win;
		}elsif($i eq 1){
			$seiseki = $lose;
		}elsif($i eq 2){
			$seiseki = $winmax;
		}elsif($i eq 6){
			$seiseki = $hrsum;
		}elsif($i eq 7){
			$seiseki = $stesum;
		}elsif($i eq 8){
			$seiseki = $errsum;
		}else{
			$game_flag = 0;
			if($win + $lose eq $league_game){
				$game_flag = 1;
			}else{
				foreach(@ranking){
			 		($saku,$pass,$home,$team,$icon,$date,$ip,$teamdata) = split /<p>/;
					($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $jiseki, $boxsum, $hitsum, $hrsum, $stesum, $errsum) = split(/<>/, $teamdata);
					if($win + $lose eq $league_game){
						$game_flag = 1;
						last;
					}
				}
			}
			if($game_flag){
				if($i eq 3){
					$seiseki = sprintf("%03d", ($hitsum / $boxsum) * 1000);
				}elsif($i eq 4){
					$seiseki = sprintf("%.2f", ($jiseki	/ $kaid)   * 27);
				}elsif($i eq 5){
					$seiseki = sprintf("%.1f", ($get 	/ $kaio)   * 27);
				}
			}else{
				$seiseki = $team = $saku = '';
			}
		}
		$rank_top[0][$i] = "$seiseki<>$team<>$saku<>$pr_dai";
	}

	@team_rank = ();
	$j=0;
	foreach(@users){
 		($saku,$pass,$home,$team,$icon,$date,$ip,$teamdata,$pointdata,$bosstype,$charadata) = split /<p>/;
		($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $jiseki, $boxsum, $hitsum, $hrsum, $stesum, $errsum) = split(/<>/, $teamdata);
		($point, $champ, $secon, $third, $y_dari, $y_hr, $y_ten, $y_ste, $p_bou, $p_win, $p_san) = split(/<>/, $pointdata);

		$game = $win + $lose;
		if($win < $delete_win){
			$_ = '';
		}else{
			if($game){		$winritu = sprintf("%03d", ($win 	/ $game)   * 1000);	}
			if($boxsum){	$daritu	 = sprintf("%03d", ($hitsum / $boxsum) * 1000);	}
			if($kaio){		$tenritu = sprintf("%.1f", ($get 	/ $kaio)   * 27);	}
			if($kaid){		$bouritu = sprintf("%.2f", ($jiseki	/ $kaid)   * 27);	}

			$team_rank[$j] = "$saku<>$home<>$team<>$icon<>$game<>$win<>$winmax<>$lose<>.$winritu<>.$daritu<>$tenritu<>$bouritu<>$hrsum<>$stesum<>$errsum";
			for($i=0; $i<8; $i++){
				($d,$d,$l_team) = split(/<>/, $lead_player[$i]);
				if($team eq $l_team){
					$lead_player[$i] = "$lead_player[$i]<>$icon";
				}
			}
			if($j eq 0){ $champ_team = $team; }
			$j++;

			$lastjun = $j;
			$teamdata  = "$lastjun<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0<>0";

			@players = split(/<c>/, $charadata);
			@player = ();
			for($i=0; $i<8; $i++){
				($id[$i], $jun[$i], $posit[$i], $yasyu[$i], $cond[$i], $pow[$i], $mit[$i], $run[$i], $def[$i]) = split(/<>/, $players[$i]);
				$player[$i] = "$s_yasyu$id[$i]<>$jun[$i]<>$posit[$i]<>$yasyu[$i]<>5<>$pow[$i]<>$mit[$i]<>$run[$i]<>$def[$i]<>0<>0<>0<>0<>0<>0<>0<>0";
			}
			for($i=8; $i<10; $i++){
				($id[$i], $jun[$i], $posit[$i], $pitch[$i], $cond[$i], $fas[$i], $cha[$i], $sei[$i], $def[$i]) = split(/<>/, $players[$i]);
				$player[$i] = "$s_pitch$id[$i]<>$jun[$i]<>$posit[$i]<>$pitch[$i]<>5<>$fas[$i]<>$cha[$i]<>$sei[$i]<>$def[$i]<>0<>0<>0<>0<>0<>0<>0";
			}
			$charadata = join('<c>', @player);

			if($team eq $y_title[0]){ $y_dari++; $point += 5; }
			if($team eq $y_title[1]){ $y_hr++; $point += 5; }
			if($team eq $y_title[2]){ $y_ten++; $point += 5; }
			if($team eq $y_title[3]){ $y_ste++; $point += 5; }
			if($team eq $p_title[0]){ $p_bou++; $point += 5; }
			if($team eq $p_title[1]){ $p_win++; $point += 5; }
			if($team eq $p_title[3]){ $p_san++; $point += 5; }
			if($j eq 1){
				$champ++;
				$point += 20;
			}elsif($j eq 2){
				$secon++;
				$point += 15;
			}elsif($j eq 3){
				$third++;
				$point += 10;
			}elsif($j eq 4){
				$point += 5;
			}elsif($j eq 5){
				$point += 3;
			}elsif($j <= 10){
				$point += 1;
			}
			$pointdata = "$point<>$champ<>$secon<>$third<>$y_dari<>$y_hr<>$y_ten<>$y_ste<>$p_bou<>$p_win<>$p_san";

			$_ = "$saku<p>$pass<p>$home<p>$team<p>$icon<p>$times<p>$ip<p>$teamdata<p>$pointdata<p>$bosstype<p>$charadata<p><p>0<p>\n";
		}
	}
	$league_winner  = $users[0];

	truncate (US, 0);
	seek(US,0,0);	print US @users;
	close(US);
	eval 'flock(US,8);';

# 백업파일 기입
	open(UB,"+<$leaguefold/$userbackfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(UB,2);';
	truncate (UB, 0);
	seek(UB,0,0);	print UB @users;
	close(UB);
	eval 'flock(UB,8);';

# 기록실파일 갱신 처리
	open(RC,"+<$leaguefold/$recordfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(RC,2);';

	@records = <RC>;
	if(!$records[0]){
		$records[0] = "<d><d><d><d><d><d><d><d>\n";
		$records[1] = "<d><d><d><d><d><d>\n";
		$records[2] = "<d><d><d><d><d><d>\n";
		$records[3] = "<d><d><d><d><d><d>\n";
		$records[4] = "<d><d><d><d><d><d><d><d><d>\n";
		$records[5] = "<d><d><d><d><d><d>\n";
		$records[6] = "<d><d><d><d><d><d><d>\n";
	}
	for($i=0; $i<3; $i++){
		@kiroku = split(/<d>/, $records[$i+4]);
		$j = 0;
		foreach $check (@kiroku){
			if(	(	(($i eq 0 && $j eq 4) || ($i eq 2 && $j eq 0))
					&&
					(	(split(/<>/, $check))[0] eq ''
						||
						(	(split(/<>/, $rank_top[$i][$j]))[0] ne ''
							&&
							(split(/<>/, $rank_top[$i][$j]))[0] <= (split(/<>/, $check))[0]
						)
					)
				)
				||
				(	(($i eq 0 && $j ne 4) || ($i eq 1) || ($i eq 2 && $j ne 0))
					&&
					(split(/<>/, $rank_top[$i][$j]))[0] ne ''
					&&
					(split(/<>/, $rank_top[$i][$j]))[0] >= (split(/<>/, $check))[0]
				)
			){
				$check = $rank_top[$i][$j];
			}
			$j++;
		}
		$records[$i+4] = join('<d>', @kiroku);
	}

	truncate (RC, 0);
	seek(RC,0,0);	print RC @records;
	close(RC);
	eval 'flock(RC,8);';

# 전회 팀 랭킹 파일 기입
	$team_rank = join("<>\n", @team_rank);
	$team_rank .= "<>\n";

	open(PT,"+<$leaguefold/$last_teamfile") || &error('지정된 파일이 열리지 않습니다. ');
	truncate (PT, 0);
	seek(PT,0,0);	print PT $team_rank;
	close(PT);

# 현재의 승리자 파일 초기화
	open(WN,"+<$leaguefold/$winfile") || &error('지정된 파일이 열리지 않습니다. ');
	truncate (WN, 0);
	seek(WN,0,0);	print WN $league_winner;
	close(WN);

# 시합의 기록 파일 초기화
	$g_log = '';

	open(LG,"+<$leaguefold/$logfile") || &error('지정된 파일이 열리지 않습니다. ');
	truncate (LG, 0);
	seek(LG,0,0);	print LG $g_log;
	close(LG);

# 코멘트 파일 기입
	open(CF,"+<$commentfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(CF,2);';

	@comments = <CF>;
	$kakiko = "1<><><>$times<>제$pr_dai회 극공간을 초월하는 리그는 $champ_team가 우승! <><>\n";

	unshift(@comments, $kakiko);
	splice(@comments, $com_max);

	truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

# 역대 랭킹 파일 기입
	$lead_player = join('<c>', @lead_player);

	$leading = "$kakiko_times<d>$pr_dai<d>$team_rank[0]<d>$lead_player<d>\n";
	splice(@past_rank,0,1,$leading);

	open(PR,"+<$past_rankfile") || &error('지정된 파일이 열리지 않습니다. ');
	eval 'flock(PR,2);';
	truncate (PR, 0);
	seek(PR,0,0);	print PR @past_rank;
	close(PR);
	eval 'flock(PR,8);';

}#end league_end

1;
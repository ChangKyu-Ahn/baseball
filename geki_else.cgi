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


##### ��ŷ ���
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
<input type="submit" name="league_rank" value="ǥ��">
</form>

_EOF_

}#end rank_head

##### �� ��ŷ ���
sub team_rank{

	open(US,"$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

	print "������ ���� ��ŷ(���� 20 ��)����<BR>\n";
	print "<table border=1 width=$ysize cellspacing=0>\n";
	print "<tr align=\"center\"><td><br></td><td>��(������ ����)</td><td>����</td><td>�¸�</td><td>�й�</td><td>����</td><td>�·�</td><td>Ÿ��</td><td>�����</td><td>������</td><td>Ȩ��</td><td>����</td><td>��å</td><td>����</td></tr>\n";
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
			print "<option>[$ii] $game ���� $win�� $lose�� $team\n";
		}
	}
	if($select_flag){ print "</select></form>\n"; }
	else{ print "</table><br>\n"; }

	print <<"_EOF_";

<form action="$cgifile" method="$method">
<input type="hidden" name="league_rank" value=1>
<input type="hidden" name="no" value=$no>
<input type="submit" name="win"  value="�¸�">
<input type="submit" name="lose" value="�й�">
<input type="submit" name="max"  value="����">
<input type="submit" name="daritu" value="Ÿ��">
<input type="submit" name="loss" value="�����">
<input type="submit" name="ten"  value="������">
<input type="submit" name="hr"  value="Ȩ��">
<input type="submit" name="ste" value="����">
<input type="submit" name="err" value="��å">
</form>

_EOF_

	&footer;
	&chosaku;

}#end team_rank

##### ���� ��ŷ
sub play_rank{

# �߼�
	open(YD,"$leaguefold/$yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

# ����
	open(PD,"$leaguefold/$pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

	print "�� Ÿ�� ��<BR>������ Ÿ������$kitei_hit(���� * 25)��<br><table border=1 width=\"$ysize\" cellspacing=0>\n";
	print "<tr align=\"center\"><td><br></td><td>����</td><td>Ÿ��</td><td>Ÿ��</td><td>Ÿ��</td><td>��Ÿ</td><td>Ȩ��</td><td>Ÿ��</td><td>����</td><td>���Ÿ</td><td>����</td><td>��å</td><td>��</td></tr>\n";
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
<input type="submit" name="daritu" value="Ÿ��">
<input type="submit" name="hit" value="��Ÿ">
<input type="submit" name="hr"  value="Ȩ��">
<input type="submit" name="ten" value="Ÿ��">
<input type="submit" name="for" value="����">
<input type="submit" name="gid" value="���Ÿ">
<input type="submit" name="ste" value="����">
<input type="submit" name="err" value="��å">
</form>

_EOF_

	print "�� ���� ��<BR>������ ���� ȸ����$kitei_pit(���� * 25)��<br><table border=1 width=\"$ysize\" cellspacing=0>\n";
	print "<tr align=\"center\"><td><br></td><td>����</td><td>�����</td><td>�¸�</td><td>�й�</td><td>�·�</td><td>����</td><td>Ż����</td><td>����</td><td>��Ȩ��</td><td>��</td></tr>\n";
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
<input type="submit" name="bouritu" value="�����">
<input type="submit" name="pitwin" value="�¸�">
<input type="submit" name="pitlose" value="�й�">
<input type="submit" name="pitritu" value="�·�">
<input type="submit" name="p_san" value="Ż����">
<input type="submit" name="p_four" value="����">
<input type="submit" name="p_hrp" value="��Ȩ��">
</form>

_EOF_

	&footer;
	&chosaku;

}#end play_rank

##### �� ȹ�� ����Ʈ ��ŷ
sub point_rank{

	open(US,"$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(US,1);';
	seek(US,0,0);  @users = <US>;  close(US);
	eval 'flock(US,8);';

	&team_sort3;

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$mespoint_rank</font>
<br><br><br>
��£�20 p, 2����15 p, 3����10 p, 4����5 p, 5��~10����1 p, �� Ÿ��Ʋ��5p<br>
<table border=1 width=\"$ysize\" cellspacing=0>
<tr align=\"center\"><td>����</td><td>��</td><td>����Ʈ</td><td>���</td><td>2��</td><td>3��</td><td>��Ÿ</td><td>Ȩ��</td><td>Ÿ��</td><td>����</td><td>���</td><td>�ֽ�</td><td>Ż����</td><td>����</td></tr>

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

##### ������ ��� ���
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
<option value=4 $select[4]>��Ͻ�(1 ����)
<option value=5 $select[5]>��Ͻ�(����)
</select>
��<input type=submit name=kiroku value="ǥ��">
</form>

_EOF_

}#end past_head

##### ��ȸ ���� ���
sub last_kekka{

	open(PR,"$past_rankfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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
<font size=5 color="#FF0000"><b>��$pr_daiȸ �ذ����� �ʿ��ϴ� ���״� $team�� ���! </b></font>
<br><br><br>

<table width=60%>
	<tr align=center>
	$icon_pri
	<td><br><font size=6><b>$team</b></font><br>
		<font size=3><b>������$saku</b></font><br><br>
		<font size=5><b>$game ���� $win��$lose��</b></font><br><br></td>
	<tr align=center>
	<td colspan=$span>
	<table border=1 cellspacing=0 width=100% style="font-size: 14pt; font-weight: bold">
		<tr align=center>
		<td width=20%>�·�</td><td width=30%>$winritu</td><td width=20%>�ִ� ����</td><td width=30%>$winmax</td>
		</tr>
		<tr align=center>
		<td width=20%>Ÿ��</td><td width=30%>$daritu</td><td width=20%>�����</td><td width=30%>$bouritu</td>
		</tr>
		<tr align=center>
		<td width=20%>������</td><td width=30%>$tenritu</td><td width=20%>Ȩ��Ÿ</td><td width=30%>$hrsum</td>
		</tr>
		<tr align=center>
		<td width=20%>����</td><td width=30%>$stesum</td><td width=20%>��å</td><td width=30%>$errsum</td>
		</tr>
	</table>
	</td>
	</tr>
</table>
<br><br><br>

_EOF_

	print"<table width=80%>\n";

	for($i=0; $i<4; $i++){
		if($i eq 0)		{ @rankcom = ('����Ÿ��', '�ֿ�� �����'); }
		elsif($i eq 1)	{ @rankcom = ('Ȩ��Ÿ��', '�ִ� �¸�'); }
		elsif($i eq 2)	{ @rankcom = ('Ÿ����', '�ִ� ����'); }
		elsif($i eq 3)	{ @rankcom = ('�����', '�ִ�Ż����'); }

		print "<tr align=center>\n";

		for($j=0; $j<2; $j++){
			print "<td colspan=2 width=50%><br><b>�� $rankcom[$j] ��</b></td>\n";
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
			print "<tr><td>����</td><td><b>$seiseki</b></td></tr>\n";
			print "<tr><td>�̸�</td><td><b>$p_name</b></td></tr>\n";
			print "<tr><td>��</td><td><b>$team</b></td></tr></table></td>\n";
		}
		print "</tr>\n";
	}
	print "</table><br><br>\n";

	&footer;
	&chosaku;

}#end last_kekka

##### ��ȸ �� ��ŷ
sub last_team{

	open(PT,"$leaguefold/$last_teamfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(PT,0,0);  @last_teams = <PT>;  close(PT);

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meslast_team</font>
<br><br>

_EOF_

	&past_head;

	print "<table border=1 width=$ysize cellspacing=0>\n";
	print "<tr align=\"center\"><td>����</td><td>��</td><td>����</td><td>�¸�</td><td>�й�</td><td>����</td><td>�·�</td><td>Ÿ��</td><td>�����</td><td>������</td><td>Ȩ��</td><td>����</td><td>��å</td><td>����</td></tr>\n";

	$jun = 0;
	$select_flag = 0;
	foreach(@last_teams){
		($saku,$home,$team,$icon,$game,$win,$winmax,$lose,$winritu,$daritu,$tenritu,$bouritu,$hrsum,$stesum,$errsum) = split /<>/;

		$jun++;
		if($jun <= 50){
			$jun_pri = $jun;
			if($jun eq 1){
				$jun_pri = "<font color=\"FF0000\"><b>���</b></font>";
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
			print "<option>[$jun] $game ���� $win�� $lose�� $team\n";
		}
	}

	if($select_flag){ print "</select></form><br>\n"; }
	else{ print "</table><br><br>\n"; }

	&footer;
	&chosaku;

}#end last_team

##### ��ȸ ���� ��ŷ
sub last_play{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meslast_play</font>
<br><br>

_EOF_

	open(LY,"$leaguefold/$last_yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(LY,0,0);  @{$last_player[0]} = <LY>;  close(LY);

	open(LP,"$leaguefold/$last_pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(LP,0,0);  @{$last_player[1]} = <LP>;  close(LP);

	&past_head;

	print "<table width=\"$ysize\">\n";

	for($j=0; $j<4; $j++){
		if($j eq 0)		{ @rankcom = ('Ÿ��', '�����');	@ranktop = ('Ÿ��', '�����'); }
		elsif($j eq 1)	{ @rankcom = ('Ȩ��Ÿ', '�¸�');	@ranktop = ('Ȩ��Ÿ', '�¸�'); }
		elsif($j eq 2)	{ @rankcom = ('Ÿ��', '����');	@ranktop = ('Ÿ��', '����'); }
		elsif($j eq 3)	{ @rankcom = ('����', 'Ż����');	@ranktop = ('����', 'Ż����'); }

		print "<tr align=center>\n";
		for($i=0; $i<2; $i++){
			print "<td width=50%><br>�� $rankcom[$i] ��<table border=1 width=90% cellspacing=0>\n";
			print "<tr align=center><td>����</td><td>$ranktop[$i]</td><td>����</td><td>��</td></tr>\n";

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

##### ���� ��ŷ
sub past_rank{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$mespast_rank</font>
<br><br>

_EOF_

	&past_head;

	open(PR,"$past_rankfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(PR,0,0);  @past_rank = <PR>;  close(PR);

	print "�� ���� ��� �� ��<BR><table border=1 width=90% cellspacing=0>\n";
	print "<tr align=\"center\"><td>��</td><td>��</td><td>����</td><td>�¸�</td><td>�й�</td><td>����</td><td>�·�</td><td>Ÿ��</td><td>�����</td><td>������</td><td>Ȩ��</td><td>����</td><td>��å</td><td>����</td></tr>\n";

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
		if($i eq 0){	@rankcom = ('����Ÿ��',	'�ֿ�� �����') ;@ranktop = ('Ÿ��',	'�����'); }
		elsif($i eq 1){ @rankcom = ('Ȩ��Ÿ��',	'�ִ� �¸�');	@ranktop = ('Ȩ��Ÿ', '�¸�'); }
		elsif($i eq 2){ @rankcom = ('Ÿ����',	'�ִ� ����');	@ranktop = ('Ÿ��',	'����'); }
		elsif($i eq 3){ @rankcom = ('�����',	'�ִ�Ż����');	@ranktop = ('����',	'Ż����'); }

		print "<tr align=center>\n";
		for($j=0; $j<2; $j++){
			print "<td><br><br>�� $rankcom[$j] ��<br><table border=1 width=90% cellspacing=0>\n";
			print "<tr align=center><td>��</td><td>$ranktop[$j]</td><td>����</td><td>��</td></tr>\n";
			print "@{$play_rank[$j][$i]}";
			print "</table></td>\n";
		}
		print "</tr>\n";
	}
	print "</table><br><br>\n";

	&footer;
	&chosaku;

}#end past_rank

##### ��Ͻ�ǥ��
sub each_reco{

	open(RC,"$leaguefold/$recordfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	seek(RC,0,0);  @records = <RC>;  close(RC);

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">$meseach_reco</font>
<br><br>

_EOF_

	&past_head;

	@tuika1 = ('1 ����', '����');

	if($no eq 4){ &game_rec; }
	else{ &season_rec; }

	&footer;
	&chosaku;

}#end each_reco

##### 1 ���� ���
sub game_rec{

	@table_name	= ('���� ���', '�� ���', '�߼� ���', '���� ���');
	@{$bumon[0]} = ('���� ����', '�ִ� ����', '�ִ� ��Ÿ', '�ִ� Ȩ��Ÿ', '�ִ� ����', '�ִ� ����', '�ִ� ����/���庼', '�ִ� ��å');
	@{$bumon[1]} = ('�ִ� ����', '�ִ� ��Ÿ', '�ִ� Ȩ��Ÿ', '�ִ� ����', '�ִ� ����', '�ִ� ��å');
	@{$bumon[2]} = ('�ִ� ��Ÿ', '�ִ� Ȩ��Ÿ', '�ִ� Ÿ��', '�ִ� ����', '�ִ� ����', '�ִ� ��å');
	@{$bumon[3]} = ('���� ����', '����Ÿ ������ ����', '�ִ�Ż����', '�ִ� ����', '�ִ���Ȩ��Ÿ', '�ִٿ�����/���庼');
	for($i=0; $i<$#table_name+1; $i++){
		if($i < 2){ @table_top = ('��', '����'); }
		else{ @table_top = ('�̸�', '��'); }
		print "�� $tuika1[0]$table_name[$i] ��<table border=1 width=$ysize cellspacing=0>\n";
		print "<tr align=center><td>��ϸ�</td><td>���</td><td>$table_top[0]</td><td>$table_top[1]</td><td>��</td><td>�Ͻ�</td></tr>\n";

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

##### ���� ���
sub season_rec{

	@table_name	= ('�� ���', '�߼� ���', '���� ���');
	@{$bumon[0]} = ('�ִ� �¸�', '�ִ� ����', '�ִ� ����', '�ְ� Ÿ��', '�ֿ�� �����', '�ְ� ������', '�ִ� Ȩ��Ÿ', '�ִ� ����', '�ִ� ��å');
	@{$bumon[1]} = ('�ְ� Ÿ��', '�ִ� Ȩ��Ÿ', '�ִ� Ÿ��', '�ִ� ����', '�ִ� ��Ÿ', '�ִ� ��å');
	@{$bumon[2]} = ('�ֿ�� �����', '�ִ� �¸�', '�ִ� ����', '�ִ�Ż����', '�ְ� �·�', '�ִ� ����/���庼', '�ִ���Ȩ��Ÿ');
	@{$jun[0]}	= (0,1,2,3,4,5,6,7,8);
	@{$jun[1]}	= (0,1,2,4,3,5);
	@{$jun[2]}	= (0,1,4,3,2,5,6);
	for($i=0; $i<$#table_name+1; $i++){
		if($i < 1){ @table_top = ('��', '����'); }
		else{ @table_top = ('�̸�', '��'); }
		print "�� $tuika1[1]$table_name[$i] ��<table border=1 width=$ysize cellspacing=0>\n";
		print "<tr align=center><td>��ϸ�</td><td>���</td><td>$table_top[0]</td><td>$table_top[1]</td><td>��</td></tr>\n";

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

##### �� ��Ʈ��
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

##### �� ��Ʈ��
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

##### �߼� ��Ʈ ó�� �غ�
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

##### �߼� ��Ʈ ó��
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

##### ���� ��Ʈ ó�� �غ�
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

##### ���� ��Ʈ ó��
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

##### ���� �Ⱓ ���� ó��
sub league_end{

# ���� ��ŷ ���� �Ͻ� ����
	$pr_dai++;
	$kakiko_times = $times - ((($hour - $league_time + 24) % 24 ) * 3600 + $min * 60 + $sec);
	$kakiko = "$kakiko_times<d>-1<d><d><d>\n";
	splice(@past_rank,0,0,$kakiko);

	open(PR,"+<$past_rankfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(PR,2);';
	truncate (PR, 0);
	seek(PR,0,0);	print PR @past_rank;
	close(PR);
	eval 'flock(PR,8);';

	$league_day = $league_limit;

	$kitei_hit = $league_day * 25;
	$kitei_pit = $league_day * 25;

	@rank_top = ();

# �߼� ���� �ʱ�ȭ
	open(YD,"+<$leaguefold/$yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

	open(LY,"+<$leaguefold/$last_yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(LY,2);';
	truncate (LY, 0);
	seek(LY,0,0);	print LY @last_yasyu;
	close(LY);
	eval 'flock(LY,8);';

# ���� ���� �ʱ�ȭ
	open(PD,"+<$leaguefold/$pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

	open(LP,"+<$leaguefold/$last_pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(LP,2);';
	truncate (LP, 0);
	seek(LP,0,0);	print LP @last_pitch;
	close(LP);
	eval 'flock(LP,8);';

# ���� ���� �ʱ�ȭ
	open(US,"+<$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

# ������� ����
	open(UB,"+<$leaguefold/$userbackfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(UB,2);';
	truncate (UB, 0);
	seek(UB,0,0);	print UB @users;
	close(UB);
	eval 'flock(UB,8);';

# ��Ͻ����� ���� ó��
	open(RC,"+<$leaguefold/$recordfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

# ��ȸ �� ��ŷ ���� ����
	$team_rank = join("<>\n", @team_rank);
	$team_rank .= "<>\n";

	open(PT,"+<$leaguefold/$last_teamfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	truncate (PT, 0);
	seek(PT,0,0);	print PT $team_rank;
	close(PT);

# ������ �¸��� ���� �ʱ�ȭ
	open(WN,"+<$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	truncate (WN, 0);
	seek(WN,0,0);	print WN $league_winner;
	close(WN);

# ������ ��� ���� �ʱ�ȭ
	$g_log = '';

	open(LG,"+<$leaguefold/$logfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	truncate (LG, 0);
	seek(LG,0,0);	print LG $g_log;
	close(LG);

# �ڸ�Ʈ ���� ����
	open(CF,"+<$commentfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(CF,2);';

	@comments = <CF>;
	$kakiko = "1<><><>$times<>��$pr_daiȸ �ذ����� �ʿ��ϴ� ���״� $champ_team�� ���! <><>\n";

	unshift(@comments, $kakiko);
	splice(@comments, $com_max);

	truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

# ���� ��ŷ ���� ����
	$lead_player = join('<c>', @lead_player);

	$leading = "$kakiko_times<d>$pr_dai<d>$team_rank[0]<d>$lead_player<d>\n";
	splice(@past_rank,0,1,$leading);

	open(PR,"+<$past_rankfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(PR,2);';
	truncate (PR, 0);
	seek(PR,0,0);	print PR @past_rank;
	close(PR);
	eval 'flock(PR,8);';

}#end league_end

1;
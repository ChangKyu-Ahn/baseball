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


##### �α��� ȭ��
sub login{

	$userdata = &user_check;

	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata, $gamedata, $campflag) = split(/<p>/, $userdata);
	($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $t_jiseki, $boxsum, $hitsum, $horsum, $stesum, $errsum) = split(/<>/, $teamdata);
	@bosstype = split(/<>/, $bosstype);
	$gamedate = &date($date);

	$game = $win + $lose;
	$game_nokori = $league_game - $game;
	if($game_nokori <= 10){
		if($game_nokori <= 0){ $game_nokori = "���� ����"; }
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
		if($cond[$i] < 2)	{ $condition[$i] = "�־�"; $condition_bar[$i] = $cond_bar[0]; }
		elsif($cond[$i] < 4){ $condition[$i] = "����"; $condition_bar[$i] = $cond_bar[1]; }
		elsif($cond[$i] < 6){ $condition[$i] = "����"; $condition_bar[$i] = $cond_bar[2]; }
		elsif($cond[$i] < 8){ $condition[$i] = "ȣ��"; $condition_bar[$i] = $cond_bar[3]; }
		else				{ $condition[$i] = "��ȣ"; $condition_bar[$i] = $cond_bar[4]; }
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
<font size=5><b>$team</b> <font size=4><b>������</b></font> <font color="FF0000" size=5><b>$user_jun��</b></font></font><br>
[ ���� ���� �Ͻ� - $gamedate ]
<table width="$ysize">
	<tr align="center">
	<td width="35%">
	<table border=1 width="100%" height=100%>
		<tr align=center>
		<td>
		$icon_pri
		���� �� $saku
		<table width="100%">
			<tr align=center>
			<td colspan=3>Ÿ��(1~10)</td>
			</tr>
			<tr align=center>
			<td>������</td>
			<td><select name=b_act>@{$bonuslist[0]}</select></td>
			<td>������</td>
			</tr>
			<tr align=center>
			<td>��Ʈ(��)</td>
			<td><select name=b_bnt>@{$bonuslist[1]}</select></td>
			<td>��Ʈ(��)</td>
			</tr>
			<tr align=center>
			<td>����(��)</td>
			<td><select name=b_ste>@{$bonuslist[2]}</select></td>
			<td>����(��)</td>
			</tr>
			<tr align=center>
			<td>������</td>
			<td><select name=b_mnd>@{$bonuslist[3]}</select></td>
			<td>����</td>
			</tr>
		</table>
		</td>
		</tr>
	</table>
	</td>
	<td width="65%">
	<table border=1 width="100%" height="20%">
		<tr align=center>
		<td>����</td>
		<td>�·�</td>
		<td>�¸�</td>
		<td>�й�</td>
		<td>����</td>
		<td>���� ����</td>
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
		<td>Ÿ��</td>
		<td>�����</td>
		<td>������</td>
		<td>Ȩ��Ÿ</td>
		<td>����</td>
		<td>��å</td>
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
		<td colspan=3>�ֱ� 5 ������ ���</td>
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
		<td>��</td><td>��</td><td>�̸�</td><td>����</td><td>�Ŀ�</td><td>��Ȯ��</td><td>�޸���</td><td>����</td><td>�հ�</td><td>Ÿ��</td><td>Ȩ��</td><td>Ÿ��</td><td>����</td><td>���Ÿ</td><td>����</td><td>��å</td>
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
		<td>��</td><td>��</td><td>�̸�</td><td>����</td><td>�ӱ�</td><td>��ȭ</td><td>����</td><td>����</td><td>�հ�</td><td>�����</td><td>�¸�</td><td>�й�</td><td>Ż����</td><td>����</td><td>�ǹ�Ʈ</td>
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
		print "���� ��� ȭ���Դϴ�. \n";
	}elsif($win + $lose >= $league_game){
		print "��ȸ�� ���״� $league_game ���ձ�����. ������ ���װ� ���۵� ������ ��ٸ��� �־�. \n";
	}elsif(($times - $date) < $between * 60 && $win + $lose > 0){
		$nexttimes  = $date + ($between + 1) * 60 - $times;
		$nextminits = int($nexttimes / 60);
		print "������ ���ձ��� $nextminits�� ���� ��ٸ��� �־�. \n";
	}else{
		print "<input type=submit name=playkaku value=\"���� ����\">\n";
		if($campflag < $camp_limit){
			print "����<input type=submit name=campin value=\"ķ�� ��\">\n";
		}
		print "\n";
	}

	print <<"_EOF_";
<br><br><br>
<input type=hidden name=saku value="$saku">
<input type=hidden name=pass value="$pass">
<input type=submit name=delekaku value="���� ����">
<br>

_EOF_

	&footer;
	&chosaku;

}#end login

##### ���� ��� Ȯ��
sub playkaku{

	@bosspara	= ($form{'b_act'},$form{'b_bnt'},$form{'b_ste'},$form{'b_mnd'});

# �� ĳ������ üũ
	for($i=0; $i<10; $i++){
		$dajun[$i] = $form{"jun$i"};
		if($dajun[$i] ne int($dajun[$i])){ &error('Ÿ���� ������ �Է���. '); }
		if($i < 8){
			if($dajun[$i] < 1 || $dajun[$i] > 8){ &error('Ÿ���� Ÿ���� 1~8���� ��. '); }
		}else{
			if($dajun[$i] < 9 || $dajun[$i] > 10){ &error('������ Ÿ���� 9~10���� ��. '); }
		}
		for($j=0; $j<$i; $j++){	if($dajun[$i] eq $dajun[$j]){ &error('Ÿ���� �ߺ� �ϰ� �־�. '); } }
	}

	$userdata = &user_check;

	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata) = split(/<p>/, $userdata);
	($lastjun, $win, $wincon, $winmax, $lose, $kaio, $kaid, $get, $loss, $t_jiseki, $boxsum, $hitsum, $horsum, $runsum, $errsum) = split(/<>/, $teamdata);

	if(($times < $date + $between * 60) && ($win + $lose > 0)){ &error('�������� ������ �� �� ����. '); }

	@players = split(/<c>/, $charadata);
	for($i=0; $i<10; $i++){
		$j = $dajun[$i] - 1;
		($id[$j], $jun[$j], $posit[$j], $p_name[$j], $cond[$j], $para1[$j], $para2[$j], $para3[$j], $para4[$j]) = split(/<>/, $players[$i]);
	}

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">���� ��� Ȯ��</font>
<br><br>�̰����� ���տ� �����ص� �����ϱ�? <br>(���ƿ� ���� �������� �ڷΰ���΢�)<br><br>

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

	print "<input type=submit name=playball value=\"���� ����\"></form>\n";

	&touroku_table;
	&chosaku;

}#end playkaku

##### ķ�� ȭ��
sub campin{

	$userdata = &user_check;

	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata, $gamedata, $campflag) = split(/<p>/, $userdata);
	($lastjun, $win, $d, $d, $lose) = split(/<>/, $teamdata);
	@bosstype	= split(/<>/, $bosstype);

	@players	= split(/<c>/, $charadata);
	@positlist	= @parasum = ();
	@positname	= ('����','1���','2���','3���','���ݼ�','���ͼ�','�߰߼�','���ͼ�');
	for($i=0; $i<10; $i++){
		($id[$i], $jun[$i], $posit[$i], $p_name[$i], $cond[$i], $para1[$i], $para2[$i], $para3[$i], $para4[$i]) = split(/<>/, $players[$i]);

		for($j=0; $j<8; $j++) {
			$select = '';
			if($positname[$j] eq $posit[$i]){ $select = 'selected'; }
			push @{$positlist[$i]}, "<option value=\"$positname[$j]\" $select> $positname[$j] </option>";
		}
		$parasum[$i] = $para1[$i] + $para2[$i] + $para3[$i] + $para4[$i];
	}
	
	if($icon_use)	{ $icon_pri = "<tr><td>������</td><td><img src=\"$imgurl/$icon\"></td></tr>"; }
	else			{ $icon_pri = ''; }

	if(($win + $lose) eq 0){
		$camp_com = "���� ���ο� ������ �����Դϴ�. <br>��⿡ ��ġ�� �ο� �����, �������� �����սô�. <br>\n";
	}elsif(($win + $lose) eq int($league_game / 2)){
		$camp_com = "�� ���¸� �ٽ� ����, �Ĺ����� �����սô�. <br>\n";
	}else{
		$camp_com = "������ ķ�� ����Դϴ�. <br>���� ���׷��̵���, ������ ������ ��ǥ�� �սô�. <br>\n";
	}

	$camp_nokori = $camp_limit - $campflag;

	&header;
	&java_sum;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">ķ�� ��</font>
<br><br>
$camp_com
<br>
ķ�� �� ������ <font size=5 color="#FF0000"><b>$camp_nokori</b></font>ȸ
<form action="$cgifile" method="$method" name=para><br>
<table border=1 width=$ysize cellpadding=5>
	<tr>
	<td width=50%>
	<br>
	<table width=100%>
		$icon_pri
		<tr>
		<td width=100>���� �̸�</td>
		<td>$team</td>
		</tr>
		<tr>
		<td width=100>����� �̸�</td>
		<td>$saku</td>
		</tr>
		<tr>
		<td width=100>Ȩ������</td>
		<td>$home</td>
		</tr>
		<tr>
		<td width=100>�н�����</td>
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
	<input type=submit name=camp_end value="���">
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

##### ķ�� ���� ó��
sub camp_rec{

	$userdata = &user_check;
	($saku, $pass, $home, $team, $icon, $date, $ip, $teamdata, $pointdata, $bosstype, $charadata, $gamedata, $campflag) = split(/<p>/, $userdata);

	&chara_para;

# �α׿� �����ϴ� ��Ÿ���� ����
	@players = split(/<c>/, $charadata);
	for($i=0; $i<8; $i++){
		($id, $jun, $posit, $yasyu, $cond, $pow, $mit, $run, $def, $box, $hit, $ten, $hr, $ste, $err, $for, $gid) = split(/<>/, $players[$i]);
		$players[$i] = "$id<>$jun<>$posit[$i]<>$p_name[$i]<>$cond<>$para1[$i]<>$para2[$i]<>$para3[$i]<>$para4[$i]<>$box<>$hit<>$ten<>$hr<>$ste<>$err<>$for<>$gid";
	}
	for($i=8; $i<10; $i++){
		($id, $jun, $posit, $pitch, $cond, $fas, $cha, $sei, $def, $pitwin, $pitlose, $kai, $jiseki, $san, $four, $hrp) = split(/<>/, $players[$i]);
		$players[$i] = "$id<>$jun<>����<>$p_name[$i]<>$cond<>$para1[$i]<>$para2[$i]<>$para3[$i]<>$para4[$i]<>$pitwin<>$pitlose<>$kai<>$jiseki<>$san<>$four<>$hrp";
	}
	$charadata = join('<c>', @players);

	$campflag++;

# ���� ���Ͽ��� ������
	open(US,"+<$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

##### ���� ���� Ȯ�� ȭ��
sub delekaku{

	&header;

	print <<"_EOF_";
<font color="$tcolor" size="$tsize">�� �������� ����</font>
<br><br>�� �����͸� �����մϴ�. �����ϱ�? <br>(���ƿ� ���� �������� �ڷΰ���΢�)<br><br>

<form action="$cgifile" method="$method">
<input type=hidden name=saku value="$form{'saku'}">
<input type=hidden name=pass value="$form{'pass'}">
<input type=submit name=delete value="�����Ѵ�">
</form>
<br><br>

_EOF_

	&chosaku;

}#end delekaku

##### ���� ���� ó��
sub delete{

	open(US,"+<$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

	open(YD,"+<$leaguefold/$yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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

	open(PD,"+<$leaguefold/$pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
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


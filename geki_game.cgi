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


##### ���� ��� ȭ��
sub playlog{

	$userdata = &user_check;
	($saku[0], $pass[0], $home[0], $team[0], $icon[0], $date[0], $ip[0], $teamdata[0], $pointdata[0], $bosstype, $charadata, $gamedata[0], $campflag[0]) = split(/<p>/, $userdata);
	($lastjun[0], $win[0], $wincon[0], $winmax[0], $lose[0], $kaio[0], $kaid[0], $get[0], $loss[0], $t_jiseki[0], $boxsum[0], $hitsum[0], $hrsum[0], $stesum[0], $errsum[0]) = split(/<>/, $teamdata[0]);

	if(($times < $date[0] + $between * 60) && ($win[0] + $lose[0] > 0)){ &error('�������� ������ �� �� ����. '); }

	$bosstype[0] = "$form{'b_act'}<>$form{'b_bnt'}<>$form{'b_ste'}<>$form{'b_mnd'}";

	@players = split(/<c>/, $charadata);
	for($i=0; $i<10; $i++){
		$dajun[$i] = $form{"jun$i"};
		$j = $dajun[$i] - 1;
		$jun[0][$j]	= $dajun[$i];
		if($i < 8){
			($id[0][$j], $d, $posit[0][$j], $yasyu[0][$j], $cond[0][$j], $pow[0][$j], $mit[0][$j], $run[0][$j], $def[0][$j], $box[0][$j], $hit[0][$j], $ten[0][$j], $hr[0][$j], $ste[0][$j], $err[0][$j], $for[0][$j], $gid[0][$j]) = split(/<>/, $players[$i]);
			$player[0][$j]	= "$id[0][$j]<>$jun[0][$j]<>$posit[0][$j]<>$yasyu[0][$j]<>$cond[0][$j]<>$pow[0][$j]<>$mit[0][$j]<>$run[0][$j]<>$def[0][$j]<>$box[0][$j]<>$hit[0][$j]<>$ten[0][$j]<>$hr[0][$j]<>$ste[0][$j]<>$err[0][$j]<>$for[0][$j]<>$gid[0][$j]";
		}else{
			($id[0][$j], $d, $posit[0][$j], $pitch[0][$j], $cond[0][$j], $fas[0][$j], $cha[0][$j], $sei[0][$j], $def[0][$j], $pitwin[0][$j], $pitlose[0][$j], $kai[0][$j], $jiseki[0][$j], $san[0][$j], $four[0][$j], $hrp[0][$j]) = split(/<>/, $players[$i]);
			$player[0][$j]	= "$id[0][$j]<>$jun[0][$j]<>$posit[0][$j]<>$pitch[0][$j]<>$cond[0][$j]<>$fas[0][$j]<>$cha[0][$j]<>$sei[0][$j]<>$def[0][$j]<>$pitwin[0][$j]<>$pitlose[0][$j]<>$kai[0][$j]<>$jiseki[0][$j]<>$san[0][$j]<>$four[0][$j]<>$hrp[0][$j]";
			$yasyu[0][$j]	= $pitch[0][$j];
		}
	}
	$charadata[0] = join('<c>', @{$player[0]});

	$userdata[0] = "$saku[0]<p>$pass[0]<p>$home[0]<p>$team[0]<p>$icon[0]<p>$date[0]<p>$ip[0]<p>$teamdata[0]<p>$pointdata[0]<p>$bosstype[0]<p>$charadata[0]<p>$gamedata[0]<p>$campflag[0]<p>\n";

	open(WN,"$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(WN,1);';
	seek(WN,0,0);  @winners = <WN>;  close(WN);
	eval 'flock(WN,8);';

	if(!$winners[0]){
		open(WN,"+<$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
		truncate (WN, 0);
		seek(WN,0,0);	print WN $userdata[0];
		close(WN);

		&error('������ �¸��ڰ� ���� ������, ������ �ǽ��� �� �������ϴ�. ');
	}

	($saku[1], $pass[1], $home[1], $team[1], $icon[1], $date[1], $ip[1], $teamdata[1], $pointdata[1], $bosstype[1], $charadata[1], $gamedata[1], $campflag[1]) = split(/<p>/, $winners[0]);
	if($saku[1] eq $saku[0] && $pass[1] eq $pass[0]){ &error('�ڽ��� ������ ������ �� ����. '); }

	($lastjun[1], $win[1], $wincon[1], $winmax[1], $lose[1], $kaio[1], $kaid[1], $get[1], $loss[1], $t_jiseki[1], $boxsum[1], $hitsum[1], $hrsum[1], $stesum[1], $errsum[1]) = split(/<>/, $teamdata[1]);

	$end_flag = 0;
	if($win[1] + $lose[1] >= $league_game){ $end_flag = 1; }

	@{$player[1]} = split(/<c>/, $charadata[1]);
	for($i=0; $i<8; $i++){
		($id[1][$i],$jun[1][$i], $posit[1][$i], $yasyu[1][$i], $cond[1][$i], $pow[1][$i], $mit[1][$i], $run[1][$i], $def[1][$i], $box[1][$i], $hit[1][$i], $ten[1][$i], $hr[1][$i], $ste[1][$i] ,$err[1][$i], $for[1][$i], $gid[1][$i]) = split(/<>/, $player[1][$i]);
	}
	for($i=8; $i<10; $i++){
		($id[1][$i],$jun[1][$i], $posit[1][$i], $pitch[1][$i], $cond[1][$i], $fas[1][$i], $cha[1][$i], $sei[1][$i], $def[1][$i], $pitwin[1][$i], $pitlose[1][$i], $kai[1][$i], $jiseki[1][$i], $san[1][$i], $four[1][$i], $hrp[1][$i]) = split(/<>/, $player[1][$i]);
		$yasyu[1][$i]   = $pitch[1][$i];
	}

# �� ����
	open(GL,"+<$leaguefold/$lockfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(GL,2);';

	@gamelock = <GL>;

	($gamecheck, $gametime) = split(/<>/, $gamelock[0]);
	if($gamecheck eq 0 || $times > $gametime + 60 * 2){
		$gamelock = "1<>$times<>\n";
	}else{
		&error('���� �������Դϴ�. �� �� ��ٸ��� �־�. ');
	}

	truncate (GL, 0);
	seek(GL,0,0);	print GL $gamelock;
	close(GL);
	eval 'flock(GL,8);';

	@team_pri = @team_d_pri = @sensyu_pri = ();
	for($i=0; $i<2; $i++){
		$game = $win[$i] + $lose[$i];
		if($icon_use){
			$icon_pri = "<img src=\"$imgurl/$icon[$i]\"><br>";
		}else{
			$icon_pri = '';
		}
		if($i eq 1){
			$rensyo_pri = "($wincon[$i]������)";
		}else{
			$rensyo_pri = "<br>";
		}
		$team_pri[$i] = "$icon_pri<b>$team[$i]</b><br>$saku[$i]<br>[ $game ���� $win[$i]��$lose[$i]�� ]<br>$rensyo_pri";

		if($game){
			$t_dari = sprintf("%03d", ($hitsum[$i] / $boxsum[$i]) * 1000);
			if($t_dari eq 1000){
				$t_dari = "1.000";
			}else{
				$t_dari = ".$t_dari";
			}
			$t_bori	= sprintf("%.2f", ($loss[$i] / $kaid[$i]) * 27);
			$t_ten	= sprintf("%0.1f", ($get[$i] / $kaio[$i]) * 27);
		}else{
			$t_dari = ".000";
			$t_bori = "0.00";
			$t_ten  = "0.0";
		}
		$team_d_pri[$i][0] = "<table border=1 width=100% cellspacing=0>";
		$team_d_pri[$i][1] = "<tr align=center><td>Ÿ��</td><td>�����</td><td>������</td><td>Ȩ��</td><td>����</td><td>��å</td></tr>";
		$team_d_pri[$i][2] = "<tr align=center><td>$t_dari</td><td>$t_bori</td><td>$t_ten</td><td>$hrsum[$i]</td><td>$stesum[$i]</td><td>$errsum[$i]</td></tr>";
		$team_d_pri[$i][3] = "</table>";

		$sensyu_pri[$i][0] = "<table border=1 width=100% cellspacing=0>";
		$sensyu_pri[$i][1] = "<tr align=center><td>����</td><td>��ġ</td><td>�̸�</td><td>����</td><td>Ÿ��</td><td>Ÿ��</td></tr>";
		for($j=0; $j<9; $j++){
			if	 ($cond[$i][$j] < 2){ $condition = "�־�"; }
			elsif($cond[$i][$j] < 4){ $condition = "���ڴ�"; }
			elsif($cond[$i][$j] < 6){ $condition = "����"; }
			elsif($cond[$i][$j] < 8){ $condition = "ȣ��"; }
			else					{ $condition = "��ȣ"; }

			$jun = $j + 1;
			if($j < 8 && $box[$i][$j]){
				$daritu = sprintf("%03d", ($hit[$i][$j] / $box[$i][$j]) * 1000);
				if($daritu eq 1000){
					$daritu = "1.000";
				}else{
					$daritu = ".$daritu";
				}
			}elsif($j eq 8){
				$daritu = "-"; $hr[$i][8] = "-";
			}else{
				$daritu = ".000";
			}
			$sensyu_pri[$i][$j+2] = "<tr align=center><td>$jun</td><td>$posit[$i][$j]</td><td>$yasyu[$i][$j]</td><td>$condition</td><td>$daritu</td><td>$hr[$i][$j]</td></tr>";
		}
		$sensyu_pri[$i][11] = "</table>";
	}

	@log = ();
	$m = 0;

	$log[$m] = "<font color=\"$tcolor\" size=\"$tsize\">������ ���</font>";
	$m++;
	$log[$m] = "<br><br><br><br><table width=75%>";
	$m++;
	$log[$m] = "<tr align=center><td width=45%><font color=\"#498248\" size=5><b>��������</b></font></td><td width=10%></td><td width=45%><font color=\"#498248\" size=5><b>���İ���</b></font></td></tr>";
	$m++;
	$log[$m] = "<tr align=center><td width=45%><br>$team_pri[0]</td><td width=10%><b>VS</b></td><td width=45%><br>$team_pri[1]</td></tr>";
	$m++;
	$log[$m] = "<tr align=center><td colspan=3>�� �� ������ ��</td></tr>";
	$m++;
	$log[$m] = "<tr align=center><td width=45%>@{$team_d_pri[0]}</td><td width=10%></td><td width=45%>@{$team_d_pri[1]}</td></tr>";
	$m++;
	$log[$m] = "<tr align=center><td colspan=3><br>�� ���� ��� ��</td></tr>";
	$m++;
	$log[$m] = "<tr align=center><td width=45%>@{$sensyu_pri[0]}</td><td width=10%></td><td width=45%>@{$sensyu_pri[1]}</td></tr>";
	$m++;
	$log[$m] = "</table>";
	$m++;

	$log[$m] = "<br><br><br>";
	$m++;

	&game_syori;
	&game_end;

	&header;

	$comsize = $comleng * 2;
	print <<"_EOF_";
@log
<form action="$cgifile" method="$method">
���� ���� ���� �ڸ�Ʈ($comleng ���ڱ���)<br>
<input type=text name=comtext size=$comsize><br><br>
<input type=hidden name=comment value=1>
<input type=hidden name=saku value="$saku[0]">
<input type=hidden name=pass value="$pass[0]">
<input type=hidden name=home value="$home[0]">
<input type=hidden name=team0 value="$team[0]">
<input type=hidden name=team1 value="$team[1]">
<input type=hidden name=ten0 value="$tokuten[0]">
<input type=hidden name=ten1 value="$tokuten[1]">
<input type=submit name=comment value="�ڸ�Ʈ ���">
</form>

_EOF_

	&footer;
	&chosaku;

}#end playlog

##### ���� ó��
sub game_syori{

	srand(time ^ ($$ + ($$ << 15)));

	@tokuten	= (0,0);
	$number		= (0,0);	# Ÿ��
	$kougeki	= 0;		# 0:��,1:��

	@g_box		= ();
	@g_hit		= ();
	@g_ten		= ();
	@g_hr		= ();
	@g_ste		= ([0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]);
	@g_san		= ();
	@g_err		= ([0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]);
	@g_four		= ();
	@g_gid		= ();
	@g_jiseki	= ();
	@kai_hit	= ([0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,x]);
	@kai_ten	= ([0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,x]);

	@kai_out	= ();
	@total_box	= (0,0);
	@total_hit	= (0,0);
	@total_ten	= (0,0);
	@total_hr	= (0,0);
	@total_ste	= (0,0);
	@total_err	= (0,0);
	@total_four	= (0,0);
	@total_gid	= (0,0);
	@total_san	= (0,0);

	@kekka_pri	= ();
	@jun_pri = @name_pri = @run_pri = @taisen_pri = @out_pri = @ten_pri = ();

	$tensa1  = 0;
	$tensa2  = 0;
	$sayonara = 0;
	$count  = 0;
	$kai     = int($count / 2 + 1);
	$kougeki = int($count % 2);		# 0:��, 1:��
	until(($kai eq 9 && $kougeki && $tensa2 < 0) || ($kai > 9 && !$kougeki && $tensa2)){ ## ���� ����

		$tensa1 = $tokuten[0] - $tokuten[1];

		@motivate = ();
		$runner   = 0;
		$run_play = 0;
		$outcount = 0;
		$kai_hit  = 0;
		$kai_ten  = 0;
		$taisen  = '';
		$kai_jun = 0;
		while($outcount < 3){
			$number[$kougeki] %= 9;
			$box = 1;
			$tuikaten = 0;
			$hit = $hr = $ten = $san = $ste = $err = $four = $gid = 0;
			$steal = $wpit = 0;

			&syori($bosstype[$kougeki], $bosstype[1-$kougeki], $player[$kougeki][$number[$kougeki]], $player[$kougeki][$run_play], $charadata[1-$kougeki], $number[$kougeki]);

			if($steal || $wpit){
				if($steal){
					$g_ste[$kougeki][$ste_play]	+= $ste;
					$total_ste[$kougeki]		+= $ste;
				}
			}else{
				$g_box[$kougeki][$number[$kougeki]]	+= $box;
				$g_hit[$kougeki][$number[$kougeki]]	+= $hit;
				$g_hr[$kougeki][$number[$kougeki]]	+= $hr;
				$g_four[$kougeki][$number[$kougeki]]+= $four;
				$g_san[$kougeki][$number[$kougeki]]	+= $san;
				$g_gid[$kougeki][$number[$kougeki]]	+= $gid;
				$g_err[1-$kougeki][$defence]		+= $err;
				$kai_hit += $hit;

				$total_box[$kougeki] += $box;
				$total_hit[$kougeki] += $hit;
				$total_hr[$kougeki]  += $hr;
				$total_err[1-$kougeki] += $err;
				$total_four[$kougeki]  += $four;
				$total_gid[$kougeki]   += $gid;
				$total_san[$kougeki]   += $san;

				if(!$err){
					$g_ten[$kougeki][$number[$kougeki]]	+= $ten;
					$total_ten[$kougeki] += $ten;
				}
				$number[$kougeki]++;
			}
			$kai_ten += $ten;
			$tokuten[$kougeki] += $tuikaten;
			if(!$err){
				$g_jiseki[1-$kougeki] += $ten;
			}

			$tensa2   = $tokuten[0] - $tokuten[1];
			if($kougeki && $kai > 8 && $tensa2 < 0){ $sayonara = 1; last; }
		}

		$kai_out[$kougeki] += $outcount;
		$kai_hit[$kougeki][$kai - 1] += $kai_hit;
		$kai_ten[$kougeki][$kai - 1] += $kai_ten;

		$ten_pri = "<font size=4><b>$tokuten[$kougeki]</b></font>";
		if($kai_ten){
			$ten_pri = "<font size=5 color=\"FF0000\"><b>$tokuten[$kougeki]</b></font>";
		}

		$tuika = '';
		if($sayonara){
			$kai_ten[1][$kai-1] = "$kai_ten[1][$kai-1]<font size=2>x</font>";
			$tuika = "<br><font size=5 color=\"FF0000\"><b>Bye Bye��~! </b></font>";
		}elsif($tensa1 && !$tensa2){
			$tuika = "<br><font size=4 color=\"FF0000\"><b>�� ȸ $kai_ten��!  ����! </b></font>";
		}elsif(($tensa1 < 0 && $tensa2 > 0) || ($tensa1 > 0 && $tensa2 < 0)){
			$tuika = "<br><font size=4 color=\"FF0000\"><b>�� ȸ $kai_ten��!  ����! </b></font>";
		}elsif(($tensa1 eq 0 && $tensa2 > 0) || ($tensa1 eq 0 && $tensa2 < 0)){
			if(!$tokuten[0] || !$tokuten[1]){
				$tuika = "<br><font size=4 color=\"FF0000\"><b>$kai_ten�� ����! </b></font>";
			}else{
				$tuika = "<br><font size=4 color=\"FF0000\"><b>$kai_ten�� ����! </b></font>";
			}
		}

		$ten_pri[$kougeki][$kai-1] = "$ten_pri$tuika";

		$count++;
		$kai     = int($count / 2 + 1);
		$kougeki = int($count % 2);
	}

	&kekka;

}#end game_syori

##### Ÿ��-���� ����
sub syori{

	local ($k_boss, $d_boss, $k_player, $r_runner, $d_charadata, $number) = @_;

	if($tensa1 > 8 || $tensa1 < -8){
		$motivate[$kougeki] = -2; $motivate[1-$kougeki] = -1;
	}

	($k_b_act, $k_b_bnt, $k_b_ste, $k_b_mnd) = split(/<>/, $k_boss);
	($d_b_act, $d_b_bnt, $d_b_ste, $d_b_mnd) = split(/<>/, $d_boss);

	if($number < 8){
		($dmy, $k_jun, $dmy, $k_yasyu, $k_cond, $k_pow, $k_mit, $k_run, $k_def) = split(/<>/, $k_player);

		$k_mental = $k_cond - 5;
		if($runner >= 10){ $k_mental *= 1.7; }
		if($kai >= 9)	{ $k_mental *= 1.5; }
		elsif($kai >= 7){ $k_mental *= 1.2; }

		$mental1 = rand($k_mental) * 0.05 + 1;
		$mental2 = rand($k_mental) * 0.1  + 1;

		$k_mind = (rand(10 - $k_b_mnd) - (10 - $k_b_mnd) * 0.5) * 0.4;

		$k_pow = $k_pow * $mental1 + $k_mind + $motivate[$kougeki];
		$k_mit = $k_mit * $mental2 + $k_mind + $motivate[$kougeki];

		if($k_pow > $k_mit)	{ $k_pow += ($k_b_act - 5) * 0.2; }
		else				{ $k_mit += ($k_b_act - 5) * 0.15; }
		if($k_run > 4){
			$k_run += (($k_b_act - 5) * 0.1 + $motivate[$kougeki]);
		}
	}else{
		$k_yasyu = $yasyu[$kougeki][8];
		$k_jun = 9;
		$k_pow = $k_mit = $k_run = -5;
	}
	if($run_play < 8){
		($dmy, $r_jun, $dmy, $r_yasyu, $r_cond, $r_pow, $r_mit, $r_run, $r_def) = split(/<>/, $r_runner);
	}else{
		$r_jun = 9;
		$r_yasyu = $yasyu[$kougeki][8];
		$r_run = -5;
	}

	@d_player = split(/<c>/, $d_charadata);
	for($k=0; $k<8; $k++){
		($dmy, $dmy, $d_posit[$k], $d_yasyu[$k], $d_cond[$k], $d_pow[$k], $d_mit[$k], $d_run[$k], $d_def[$k]) = split(/<>/, $d_player[$k]);
		$d_def[$k] += $motivate[1-$kougeki];
		if($d_posit[$k] eq '����')   { $catch = $k; }
		elsif($d_posit[$k] eq '1���'){ $first = $k; }
		elsif($d_posit[$k] eq '2���'){ $secon = $k; }
		elsif($d_posit[$k] eq '3���'){ $third = $k; }
		elsif($d_posit[$k] eq '���ݼ�'){ $short = $k; }
		elsif($d_posit[$k] eq '���ͼ�'){ $left  = $k; }
		elsif($d_posit[$k] eq '�߰߼�'){ $center = $k; }
		elsif($d_posit[$k] eq '���ͼ�'){ $right  = $k; }

		$d_def[$k] += (5 - $d_b_act) * 0.3;
	}
	($dmy, $d_jun, $d_posit, $d_pitch, $d_cond, $d_fas, $d_cha, $d_sei, $d_def9) = split(/<>/, $d_player[8]);
	$d_posit[8] = $d_posit;
	$d_def[8] = $d_def9;
	$pitch = 8;

	$p_mental = $d_cond - 5;
	if($runner >= 10){ $p_mental *= 1.5; $sta = 1.0; }
	if($kai >= 9)	{ $p_mental *= 1.4; $sta = 0.8; }
	elsif($kai >= 6){ $p_mental *= 1.2; $sta = 0.9; }

	$mental1 = rand($p_mental) * 0.05 + $sta;
	$mental2 = rand($p_mental) * 0.07 + $sta;
	$mental3 = rand($p_mental) * 0.1  + $sta;

	$p_mind = (rand(10 - $d_b_mnd) - (10 - $d_b_mnd) * 0.5) * 0.4;

	$d_fas = $d_fas * $mental1 + $p_mind + $motivate[1-$kougeki];
	$d_cha = $d_cha * $mental2 + $p_mind + $motivate[1-$kougeki];
	$d_sei = $d_sei * $mental3 + $p_mind + $motivate[1-$kougeki];

	if($d_fas > $d_cha)	{ $d_fas += (5 - $d_b_act) * 0.15; }
	else				{ $d_cha += (5 - $d_b_act) * 0.1; }
	$d_sei += (5 - $d_b_act) * 0.2;

# ����
	$r1 = (($r_run ** 1.6 - $r_pow)  - ($d_fas * 0.5 - $d_cha * 0.5 + $d_def[$pitch] * 0.5 + $d_def[$catch] * 0.5)) + $k_b_ste * 1.5;
	$r2 = (($r_run * 1.5 - $r_pow * 0.5) - ($d_def[$catch] * 0.7 + $d_def[$pitch] * 0.3 + $d_fas * 0.2 - $d_cha * 0.2)) + 55;

# ����
	$w = $d_fas * 0.5 + $d_cha * 1.5 - $d_sei - $d_def[$catch];

# ������ ��Ʈ
	$bunt = 0;
	if(abs($tensa1) < 5){
		if(($runner eq 1 || $runner eq 11) && ($outcount eq 0 || ($outcount eq 1 && $number ne 7))){
			if(($k_pow + $k_mit < 7 + ($k_b_bnt - 5) * 0.5) || (($number < 2 || $number > 4) && $k_pow < 5 + ($k_b_bnt - 5) * 0.4  && $k_mit < 5 + ($k_b_bnt - 5) * 0.4 && rand(10) < 7 + ($k_b_bnt - 5) * 0.4)){
				$bunt = 1;
			}
		}
	}

# ����
	$sansin0 = $d_fas * 1.5 - $d_cha * 0.5 - $d_sei * 0.1;
	$sansin1 = $k_mit * 1.5 - $k_pow * 0.5;
	$sansin  = ($sansin0 - $sansin1) * 1.5 + 11 - ($k_mental - $p_mental);

# �� ��
	$f0 = $k_pow + $k_mit * 0.5 - $k_run;
	$f1 = $d_sei + $d_cha * 0.5 - $d_fas;
	$f  = ($f0 - $f1) * 0.8 + 10 - $p_mental * 0.5;

# ����
	$h1 = $k_mit * 1.5 - $k_pow + $k_run * 0.5;
	$h2 = $d_fas - $d_cha + $d_sei;
	$h  = ($h1 - $h2) + 56 + ($k_mental - $p_mental);

	$ste_play = '';
	$ste_out  = '';
	if(rand(100) < $r1 && ($runner eq 1 || $runner eq 101) && $run_play ne 8){	# ����
		if(rand(100) < $r2){
			if($runner eq 1){ $runner = 10; }
			elsif($runner eq 101){ $runner = 110; }
			$ste++;
			$ste_play = $run_play;
			$motivate[$kougeki] += 0.1;
		}else{
			$ste_out = "���� ";
			$runner--;
			$outcount++;
		}
		$taisen = "<font color=\"0000FF\"><b>$r_yasyu <font size=4>���� $ste_out</font></b></font>";
		$steal = 1;
	}elsif(rand(100) < $w && $runner){		# ����
		$taisen = "<font color=\"FF9966\" size=3><b>��\��</b></font>";
		$runner *= 10;
		$motivate[1-$kougeki] -= 0.1;
		$wpit = 1;
	}elsif($bunt){					# ������ ��Ʈ
		$b = ((10 - $k_pow) + (10 - $k_mit) + $k_run) + 80;
		$bunt_out = '';
		if(rand(100) < $b || $number eq 8){
			$runner *= 10;
			$box--;
			$gid++;
		}else{
			$bunt_out = "���� ";
		}
		$taisen = "<font size=3 color=\"405080\"><b>���Ÿ $bunt_out</b></font>";
		$outcount++;
	}elsif(rand(100) < $sansin){	# ����
		$taisen = "<font size=3 color=\"008000\"><b>���� </b></font>";
		$san++;
		$outcount++;
	}elsif(rand(100) < $f){			# �� ��
		$taisen = "<font size=3 color=\"808000\"><b>���� </b></font>";
		if($runner eq 101){
			$runner += 10;
		}elsif($runner % 10){
			$runner = $runner * 10 + 1;
		}else{
			$runner += 1;
		}
		$box--;
		$four++;
	}elsif(rand(100) < $h){			# ����

	# Ȩ��
		$t40 = $k_pow * 1.5 - $k_mit * 0.5 - $k_run * 0.5;
		$t41 = $d_cha * 0.5 - $d_fas * 0.5 + $d_sei;
		$t4  = ($t40 - $t41) * 1.5 + 9;

	# ��Ÿ �ڽ�
		$t0	 = $k_mit * 0.3 + $k_pow * 0.5 + $k_run * 0.2;
		$t1	 = $d_cha * 0.5 - $d_fas * 0.2 + $d_sei * 0.7;
		$t	 = ($t0 - $t1) + 17;

	# Ŭ�� ��Ʈ
		$t10 = $k_mit * 0.4 + $k_pow * 0.6;
		$t11 = $d_fas * 0.2 + $d_cha * 0.5 + $d_sei * 0.3;
		$t1  = ($t10 - $t11) * 0.5 + 10;

		$defence2 = '';
		$def_flag = 1;
		&def_action;
		$def_pri = "$d_posit[$defence]";

		if(rand(100) < $t4){		# Ȩ��
			if($def_act > 11){
				$def_pri = "$d_posit[$defence2]$def_pri";
			}
			$taisen = "<font color=\"FF0066\"><font size=4>Ȩ��! </font>$def_pri</font>";
			$runner = $runner * 1000 + 1000;
			$hit++;
			$hr++;
			$motivate[$kougeki] += 0.3;
		}elsif(rand(100) < $t){		# ��Ÿ �ڽ�
			$tt0 = $k_run * 2 - $k_pow;
			$tt1 = $d_def[$defence] + $d_run[$defence];
			if($def_act > 11){
				$tt1 = ($tt1 + $d_def[$defence2] + $d_run[$defence2]) * 0.5;
				$def_pri = "$d_posit[$defence2]$def_pri";
			}
			$tt = $tt0 - $tt1;

			if(rand(100) < ($tt + 10)){			# ���Ÿ
				$taisen = "<b><font size=4>���Ÿ </font>$def_pri</b>";
				$runner = $runner * 1000 + 100;
				$motivate[$kougeki] += 0.2;
			}elsif(rand(100) < ($tt + 60)){		# �̷�Ÿ
				$taisen = "<b><font size=4>�̷�Ÿ </font>$def_pri</b>";
				if($runner >= 1 && rand($d_def[$defence]) < 3){
					$runner = $runner * 1000 + 10;
				}else{
					$runner = $runner * 100 + 10;
				}
				$motivate[$kougeki] += 0.1;
			}else{
				$taisen = "<b><font size=3>��Ʈ </font><font size=1>$def_pri</font></b>";
				if($runner >= 1 && rand($d_def[$defence]) < 4){
					$runner = $runner * 100 + 1;
				}else{
					$runner = $runner * 10 + 1;
				}
			}
			$hit++;
		}elsif(rand(100) < $t1){	# Ŭ�� ��Ʈ
			$taisen = "<b><font size=3>��Ʈ </font><font size=1>$def_pri</font></b>";
			if($runner >= 10 && rand($d_def[$defence]) < 3.5){
				$runner = $runner * 100 + 1;
			}else{
				$runner = $runner * 10 + 1;
			}
			$hit++;
		}else{		# �߼����� Ÿ���� ������ ���� ó��

			$def_flag = 0;
			&def_action;
			$def_pri = "$d_posit[$defence]";

			if($def_act < 9){			# ���߿��� Ÿ��
				$d10 = $k_pow * 0.3 + $k_mit * 0.5 + $k_run * 0.2;
				$d11 = $d_def[$defence] * 0.8 + $d_run[$defence] * 0.2;
				$d2 = (($k_run * 1.3 - $k_pow * 0.3) - $d_def[$defence]) * 1.5 + 10;
				$e1 = (10 - $d_def[$defence]) ** 1.5 * 0.6;

				if($def_act > 5){
					$def_pri = "$d_posit[$defence2]$def_pri";
					$d11 = ($d11 + $d_def[$defence2] * 0.8 + $d_run[$defence2] * 0.2) * 0.5;
					$d2 += 10;
					$e1 *= 1.5;
				}
				$d1 = ($d10 - $d11) + 25;

				if(rand(100) < $d1 && $def_act > 1){		# ��Ʈ
					$taisen = "<b><font size=3>��Ʈ </font><font size=1>$def_pri</font></b>";
					if($runner >= 10 && rand($d_def[$defence]) < 2){
						if($runner % 10 eq 1){
							$runner = ($runner - 1) * 100 + 11;
						}else{
							$runner = $runner * 100 + 1;
						}
					}else{
						$runner = $runner * 10 + 1;
					}
					$hit++;
				}elsif(rand(100) < $e1){	# ����
					$taisen = "<b><font color=\"FF9966\"><font size=3>��å </font><font size=1>$d_posit[$defence]</font></font></b>";
					if(rand(5) < 2){
						$runner = $runner * 100 + 10;
					}else{
						$runner = $runner * 10 + 1;
					}
					$err++;
					$motivate[1-$kougeki] -= 0.2;
				}elsif(rand(100) < $d2){	# ���� ��Ÿ
					$taisen = "<b><font size=3>���� ��Ÿ </font><font size=1>$def_pri</font></b>";
					$runner = $runner * 10 + 1;
					$hit++;
				}else{						# �ƿ�
					$d3 = ($d_def[$defence] + $k_run[$defence] * 0.3 - ($k_run * 1.5 - $k_pow * 0.5)) + 80;
					if(rand(100) < $d3 && ($runner % 10 eq 1) && $outcount < 2){		# ���� �÷���
						$taisen = "<b><font color=\"993300\"><font size=3>����Ÿ </font><font size=1>$def_pri</font></font></b>";
						if($runner eq 1)	{ $runner = 0; }
						elsif($runner eq 11){ $runner = 100; }
						elsif($runner eq 111){ $runner = 110; }
						elsif($runner eq 101){
							if(!$outcount){ $runner = 1000; }
							else{ $runner = 100; }
						}
						$outcount++;
					}else{
						$taisen = "�ƿ� <font size=1>$def_pri</font>";
					}
					$outcount++;
				}
			}else{							# �ܾ߿��� Ÿ��
				$d4 = (20 - ($d_def[$defence] * 0.7 + $d_run[$defence] * 1.3)) * 1.5 + 25;
				$e2 = (10 - $d_def[$defence]) ** 1.5 * 0.3;
				if($def_act > 11){
					$d4	 = ($d4 + (20 - ($d_def[$defence2] * 0.7 + $d_run[$defence2] * 1.3))) * 0.5;
					$e2 *= 1.5;
				}
				if(rand(100) < $d4){
					$taisen = "<b><font size=3>��Ʈ </font><font size=1>$def_pri</font></b>";
					if(rand($d_def[$defence]) < 2.5){
						if($runner % 10 eq 1){
							$runner = ($runner - 1) * 100 + 11;
						}else{
							$runner = $runner * 100 + 1;
						}
					}else{
						$runner = $runner * 10 + 1;
					}
					$hit++;
					if(rand(100) < $e2){		# ����
						$taisen = "$taisen<br><b><font color=\"FF9966\"><font size=3>��å </font><font size=1>$d_posit[$defence]</font></font></b>";
						$runner = $runner * 10;
						$err++;
						$motivate[1-$kougeki] -= 0.2;
					}
				}elsif(rand(100) < $e2){		# ����
					$taisen = "<b><font color=\"FF9966\"><font size=3>��å </font><font size=1>$d_posit[$defence]</font></font></b>";
					$runner = $runner * 100 + 10;
					$err++;
					$motivate[1-$kougeki] -= 0.2;
				}else{
					if($runner >= 100 && $outcount < 2){			# ��� �ö���
						$taisen = "<b><font color=\"405080\"><font size=3>��� </font><font size=1>$def_pri</font></font></b>";
						$runner += 900;
						$box--;
						$gid++;
					}else{
						$taisen = "�ƿ� <font size=1>$def_pri</font>";
					}
					$outcount++;
				}
			}
		}
	}else{
		$def_flag = 0;
		&def_action;
		$def_pri = "$d_posit[$defence]";

		$taisen = "�ƿ� <font size=1>$def_pri</font>";
		$outcount++;
	}

	&run_syori2;
	&run_syori1;

	if(!$steal && !$wpit){
		if(($hit || $err || $four) && ($runner % 10 eq 1)){
			$run_play = $k_jun - 1;
		}
		$name_pri[$kougeki][$kai-1][$kai_jun] = $k_yasyu;
		$jun_pri[$kougeki][$kai-1][$kai_jun]  = $k_jun;
	}
	$run_pri[$kougeki][$kai-1][$kai_jun]	= $run_pri;
	$taisen_pri[$kougeki][$kai-1][$kai_jun]	= $taisen;

	$out_pri = ' - ';
	if($outcount eq 1){ $out_pri = "��"; }
	elsif($outcount eq 2){ $out_pri = "00"; }
	elsif($outcount eq 3){ $out_pri = "000"; }
	$out_pri[$kougeki][$kai-1][$kai_jun] = $out_pri;
	$kai_jun++;

}#end syori

##### Ÿ���� ����
sub def_action{

	$hit1 = rand($k_pow*0.7+$k_mit*0.3);
	$hit2 = rand($k_pow*0.3+$k_mit*0.7);
	if(!$def_flag && rand($d_fas) - $hit1 > 3 && rand($d_cha) - $hit2 > 3){
		@ball = (0,1);
	}elsif(!$def_flag && rand($d_fas*0.3+$d_cha*0.6+$d_sei*0.1) > $hit1){
		if(rand($d_fas*0.3+$d_cha*0.5+$d_sei*0.2) > $hit2){ @ball = (2..5); }
		else{ @ball = (6..8); }
	}else{
		if(rand($d_fas*0.5+$d_cha*0.3+$d_sei*0.2) > $hit2){ @ball = (9..11); }
		else{ @ball = (12,13); }
	}
	$def_act = $ball[int(rand(@ball))];

	if	 ($def_act eq 0) { $defence = $pitch; }
	elsif($def_act eq 1) { $defence = $catch; }
	elsif($def_act eq 2) { $defence = $first; }
	elsif($def_act eq 3) { $defence = $secon; }
	elsif($def_act eq 4) { $defence = $third; }
	elsif($def_act eq 5) { $defence = $short; }
	elsif($def_act eq 6) { $defence = $secon; $defence2 = $first; }
	elsif($def_act eq 7) {
		if(rand(2) < 1){ $defence = $secon; $defence2 = $short; }
		else		   { $defence = $short; $defence2 = $secon; }
	}
	elsif($def_act eq 8) { $defence = $short; $defence2 = $third; }
	elsif($def_act eq 9) { $defence = $left;   }
	elsif($def_act eq 10){ $defence = $center; }
	elsif($def_act eq 11){ $defence = $right;  }
	elsif($def_act eq 12){
		if(rand(2) < 1){ $defence = $center; $defence2 = $left; }
		else		   { $defence = $left;   $defence2 = $center; }
	}
	elsif($def_act eq 13){
		if(rand(2) < 1){ $defence = $center; $defence2 = $right; }
		else		   { $defence = $right;  $defence2 = $center; }
	}

}#end def_action

##### ������ ó����
sub run_syori1{

	if($runner eq 1){
		$run_pri = "[1]";
	}elsif($runner eq 10){
		$run_pri = "[<font color=\"FF9966\"><b>2</b></font>]";
	}elsif($runner eq 100){
		$run_pri = "[<font color=\"FF9966\"><b>3</b></font>]";
	}elsif($runner eq 11){
		$run_pri = "[<font color=\"FF9966\"><b>12</b></font>]";
	}elsif($runner eq 101){
		$run_pri = "[<font color=\"FF9966\"><b>13</b></font>]";
	}elsif($runner eq 110){
		$run_pri = "[<font color=\"FF9966\"><b>23</b></font>]";
	}elsif($runner eq 111){
		$run_pri = "[<font color=\"FF9966\"><b>123</b></font>]";
	}else{
		$run_pri = " - ";
	}

}#end run_syori1

##### ������ ó����
sub run_syori2{

	$seikan = $runner / 1000;
	if($seikan >= 1000){ $tuikaten++; $seikan -= 1000; }
	if($seikan >= 100 ){ $tuikaten++; $seikan -= 100; }
	if($seikan >= 10  ){ $tuikaten++; $seikan -= 10; }
	if($seikan >= 1   ){ $tuikaten += int($seikan); }

	if($tuikaten){
		$runner %= 1000;
		$taisen = "<b>$taisen<font size=4 color=\"FF0000\"> $tuikaten��</font></b>";
		$ten += $tuikaten;
		$motivate[$kougeki] += $tuikaten * 0.2;
		$motivate[1-$kougeki] -= $tuikaten * 0.2;
	}

}#end run_syori2

##### ��� ǥ��
sub kekka{

	$log[$m] = "<br><font size=5 color=\"3366FF\"><b>�� ���� ���� ��</b></font><br>";
	$m++;

	for($i=0; $i<$#{$kai_ten[0]}+1; $i++){
		$kai = $i+1;

		if($kai eq 10){
			$log[$m] = "<br><font size=5 color=\"3366FF\"><b>�� ������ ��</b></font><br>";
			$m++;
		}

		$log[$m] = "<table border=1 cellspacing=0 width=85%><tr align=center bgcolor=\"#48BB22\"><td colspan=2>�� $kaiȸ ��</td></tr>";
		$m++;
		$log[$m] = "<tr align=center><td width=50%>��</td><td width=50%>��</td></tr>";
		$m++;
		$log[$m] = "<tr align=center>";

		for($j=0; $j<2; $j++){
			$log[$m] = "<td valign=top><table width=100%>";
			$m++;
			if($i eq 0){
				$log[$m] = "<tr align=center><td>����</td><td>�̸�</td><td>���</td><td>����</td><td>�ƿ�</td></tr>";
				$m++;
			}
			for($k=0; $k<$#{$out_pri[$j][$i]}+1; $k++){
				$log[$m] = "<tr align=center><td>$jun_pri[$j][$i][$k]</td><td>$name_pri[$j][$i][$k]</td><td>$taisen_pri[$j][$i][$k]</td><td>$run_pri[$j][$i][$k]</td><td>$out_pri[$j][$i][$k]</td></tr>";
				$m++;
			}
			$log[$m] = "</table></td>";
			$m++;
		}

		if($ten_pri[1][$i] eq ''){ $ten_pri[1][$i] = "<font size=4><b>$tokuten[1]</b></font>"; }
		$log[$m] = "</tr><tr align=center><td>$ten_pri[0][$i]</td><td>$ten_pri[1][$i]</td></tr></table><br><br>";
		$m++;
	}

	if($tensa2 > 0)	{ $jj=0; $kk=1; @kekka = ('��', '��'); }
	else			{ $jj=1; $kk=0;	@kekka = ('��', '��'); }

	$log[$m] = "<br><font size=5 color=\"3366FF\"><b>�� ���� ���� ��</b></font><br>";
	$m++;
	$log[$m] = "<br><font size=4><b>$tokuten[$jj]</b>��<b>$tokuten[$kk]</b>�� <font size=5><b>$team[$jj]</b></font> �� �¸��Դϴ�! </font><br>";
	$m++;

	@k_charadata = ();
	@seiseki = ();
	$news_kekka = '';
	for($i=0; $i<2; $i++){
		if($i eq 1 && $end_flag){
			$k_charadata[$i] = $charadata[$i];
		}else{
			@g_win = @g_lose = ();
			if($tensa2 > 0){ $g_win[0] = 1; $g_lose[1] = 1; }
			else		   { $g_win[1] = 1; $g_lose[0] = 1; }

			for($k=0; $k<8; $k++){ &koushin_yasyu; }
			for($k=8; $k<10; $k++){ &koushin_pitch;	}

			$k_charadata[$i] = join('<c>', @{$player[$i]});
		}

		&koushin_team;

		@game_data = split(/<g>/, $gamedata[$i]);
		$now_game = "$times<>$tokuten[$i] - $tokuten[1-$i]<>$team[1-$i]";
		unshift(@game_data, $now_game);
		splice(@game_data, 5);
		$gamedata[$i] = join("<g>", @game_data);

		$userdata[$i] = "$saku[$i]<p>$pass[$i]<p>$home[$i]<p>$team[$i]<p>$icon[$i]<p>$times<p>$ip[$i]<p>$teamdata[$i]<p>$pointdata[$i]<p>$bosstype[$i]<p>$k_charadata[$i]<p>$gamedata[$i]<p>$campflag[$i]<p>\n";
	}
	$seiseki[0][0] = $#{$kai_ten[0]} + 1;

	$t_width = 400 + 10 * ($#{$kai_ten[0]} - 8);
	$log[$m] = "<br><table border=1 bordercolor=\"004D11\" width=\"$t_width\" cellpadding=3 cellspacing=0 class=score>";
	$m++;
	$log[$m] = "<tr align=\"center\"><td>��</td>";
	$m++;
	for($i=1; $i<($#{$kai_ten[0]} + 2); $i++){
		$log[$m] = "<td>$i</td>";
		$m++;
	}
	$log[$m] = "<td>��</td><td>H</td><td>E</td></tr>";
	$m++;
	for($i=0; $i<2; $i++){
		$log[$m] = "<tr align=\"center\"><td> $team[$i] </td>";
		$m++;
		for($j=0; $j<$#{$kai_ten[$i]} + 1; $j++){
			$log[$m] = "<td width=10>$kai_ten[$i][$j]</td>";
			$m++;
		}
		$log[$m] = "<td width=25><b>$tokuten[$i]</b></td><td>$total_hit[$i]</td><td>$total_err[$i]</td></tr>";
		$m++;
	}
	for($i=0; $i<2; $i++){
		$log[$m] = "<tr align=\"center\">";
		$m++;
		if($i eq 0){
			$log[$m] = "<td rowspan=2><font size=1>(��Ÿ)</font></td>";
			$m++;
		}
		for($j=0; $j<$#{$kai_hit[$i]} + 1; $j++){
			$log[$m] = "<td width=10><font size=1>$kai_hit[$i][$j]</font></td>";
			$m++;
		}
		$log[$m] = "<td width=25><font size=1><b>$total_hit[$i]</b></font></td>";
		$m++;
		if($i eq 0){
			$log[$m] = "<td colspan=2 rowspan=2>��</td>";
			$m++;
		}
		$log[$m] = "</tr>";
		$m++;
	}
	$log[$m] = "</table><BR>";
	$m++;

	$log[$m] = "<table width=420>";
	$m++;
	for($i=0; $i<2; $i++){
		$log[$m] = "<tr><td>[$kekka[$i]]</td><td>$pitch[$i][8] $pitwin[$i][8]�� $pitlose[$i][8]��</td></tr>";
		$m++;
	}
	for($i=0; $i<2; $i++){
		if($i eq 0)	{ $log[$m] = "<tr><td width=65 valign=top>[Ȩ��Ÿ]</td><td>"; $m++; }
		else		{ $log[$m] = "<tr><td width=65>��</td><td>"; $m++; }
		$flag = 0;
		for($j=0; $j<9; $j++){
			if($g_hr[$i][$j]){
				for($k=0; $k<$g_hr[$i][$j]; $k++){
					if($j < 8)	{ $hr_pri = $hr[$i][$j] - $g_hr[$i][$j] + $k + 1; }
					else		{ $hr_pri = "-"; $j = 8; }
					$log[$m] = "$yasyu[$i][$j] $hr_priȣ ";
					$m++;
					$flag = 1;
				}
			}
		}
		if(!$flag){ $log[$m] = "����"; $m++; }
		$log[$m] = "</td></tr>";
		$m++;
	}
	$log[$m] = "</table>";
	$m++;

	for($i=0; $i<2; $i++){
		$game = $win[$i] + $lose[$i];
		$log[$m] = "<br><br><font size=4><b>$team[$i]</b></font> ($saku[$i])<br>[ $game ���� $win[$i]��$lose[$i]�� ]";
		$m++;
		$log[$m] = "<table border=1 width=70% cellspacing=0><tr align=center>";
		$m++;
		$log[$m] = "<td>����</td><td>��ġ</td><td>�̸�</td><td>Ÿ��</td><td>��Ÿ</td><td>Ȩ��</td><td>Ÿ��</td><td>����</td><td>����</td><td>���Ÿ</td><td>����</td><td>��å</td><td>Ÿ��</td><td>Ÿ��</td></tr>";
		$m++;

		@daritu = ();
		for($j=0; $j<9; $j++){
			$k = $j + 1;
			if($j < 8 && $box[$i][$j]){ $daritu[$j] = sprintf("%03d", ($hit[$i][$j] / $box[$i][$j]) * 1000); }
			elsif($j eq 8){ $bouritu = sprintf("%.2f", ($jiseki[$i][8] / $kai[$i][8]) * 27); $daritu[8] = "-"; $hr[$i][8] = "-"; }
			else{ $daritu = "000"; }
			$team_daritu = sprintf("%03d", ($hitsum[$i] / $boxsum[$i]) * 1000);

			$log[$m] = "<tr align=center><td>$k</td><td>$posit[$i][$j]</td><td>$yasyu[$i][$j]</td>";
			$m++;
			$log[$m] = "<td>$g_box[$i][$j]</td><td>$g_hit[$i][$j]</td><td>$g_hr[$i][$j]</td><td>$g_ten[$i][$j]</td><td>$g_san[$i][$j]</td><td>$g_four[$i][$j]</td><td>$g_gid[$i][$j]</td><td>$g_ste[$i][$j]</td><td>$g_err[$i][$j]</td><td>. $daritu[$j]</td><td>$hr[$i][$j]</td></tr>";
			$m++;
		}
		$log[$m] = "<tr align=center><td><b>��</b></td><td>-</td><td>-</td><td><b>$total_box[$i]</b></td><td><b>$total_hit[$i]</b></td><td><b>$total_hr[$i]</b></td><td><b>$total_ten[$i]</b></td>";
		$m++;
		$log[$m] = "<td><b>$total_san[$i]</b></td><td><b>$total_four[$i]</b></td><td><b>$total_gid[$i]</b></td><td><b>$total_ste[$i]</b></td><td><b>$total_err[$i]</b></td><td><b>. $team_daritu</b></td><td><b>$hrsum[$i]</b></td></tr>";
		$m++;

		$total_butter = $total_box[1-$i] + $total_four[1-$i] + $total_gid[1-$i];
		$log[$m] = "</table>";
		$m++;
		$log[$m] = "<br><table border=1 width=70% cellspacing=0>";
		$m++;
		$log[$m] = "<tr align=center><td>��ġ</td><td>�̸�</td><td>Ÿ��</td><td>�Ǿ�Ÿ</td><td>�ǹ�Ʈ</td><td>Ż����</td><td>����</td><td>����</td><td>��å</td><td>�����</td></tr>";
		$m++;
		$log[$m] = "<tr align=center><td>$posit[$i][8]</td><td>$pitch[$i][8]</td><td>$total_butter</td><td>$total_hit[1-$i]</td><td>$total_hr[1-$i]</td><td>$total_san[1-$i]</td><td>$total_four[1-$i]</td><td>$tokuten[1-$i]</td><td>$g_jiseki[$i]</td><td>$bouritu</td></tr>";
		$m++;
		$log[$m] = "</table>";
		$m++;
	}

}#end kekka

##### �߼� ������ ����
sub koushin_yasyu{

	$box[$i][$k] += $g_box[$i][$k];
	$hit[$i][$k] += $seiseki[2][0][$i][$k] = $g_hit[$i][$k];
	$ten[$i][$k] += $seiseki[2][2][$i][$k] = $g_ten[$i][$k];
	$hr[$i][$k]  += $seiseki[2][1][$i][$k] = $g_hr[$i][$k];
	$ste[$i][$k] += $seiseki[2][3][$i][$k] = $g_ste[$i][$k];
	$err[$i][$k] += $seiseki[2][5][$i][$k] = $g_err[$i][$k];
	$for[$i][$k] += $g_four[$i][$k];
	$gid[$i][$k] += $g_gid[$i][$k];
	$seiseki[2][4][$i][$k] = $g_san[$i][$k];

	if($g_win[$i] && $g_ten[$i][$k] > 6){
		if($g_hr[$i][$k] > 2){
			$news_kekka = "$team[$i]�� $yasyu[$i][$k]�� $g_hr[$i][$k]Ȩ��Ÿ $g_ten[$i][$k]Ÿ���� ������! ";
		}elsif($g_hit[$i][$k] > 3){
			$news_kekka = "$team[$i]�� $yasyu[$i][$k]�� $g_hit[$i][$k]��Ÿ $g_ten[$i][$k]Ÿ�����ν� ��Ȱ��! ";
		}
	}

	$cond_plus = (20 - int(rand(40))) * 0.1;
	$cond[$i][$k] += $cond_plus;
	if($cond[$i][$k] > 9){ $cond[$i][$k] = 9; }
	if($cond[$i][$k] < 1){ $cond[$i][$k] = 1; }

	$player[$i][$k] = "$id[$i][$k]<>$jun[$i][$k]<>$posit[$i][$k]<>$yasyu[$i][$k]<>$cond[$i][$k]<>$pow[$i][$k]<>$mit[$i][$k]<>$run[$i][$k]<>$def[$i][$k]<>$box[$i][$k]<>$hit[$i][$k]<>$ten[$i][$k]<>$hr[$i][$k]<>$ste[$i][$k]<>$err[$i][$k]<>$for[$i][$k]<>$gid[$i][$k]";

}#end koushin_yasyu

##### ���� ������ ����
sub koushin_pitch{

	if($k eq 8){
		$jun[$i][$k] = 10;
		$kk = 9;

		$pitwin[$i][$k]  += $g_win[$i];
		$pitlose[$i][$k] += $g_lose[$i];

		$kai[$i][$k]	+= $kai_out[1-$i];
		$jiseki[$i][$k]	+= $g_jiseki[$i];
		$san[$i][$k]	+= $seiseki[3][2][$i][$k] = $total_san[1-$i];
		$four[$i][$k]	+= $seiseki[3][5][$i][$k] = $total_four[1-$i];
		$hrp[$i][$k]	+= $seiseki[3][4][$i][$k] = $total_hr[1-$i];
		$seiseki[3][3][$i][$k] = $tokuten[1-$i];

		if($g_win[$i]){
			if(!$tokuten[1-$i] && !$total_hit[1-$i]){
				if(!$total_four[1-$i] && !$total_err[$i]){
					$news_kekka = "$team[$i]�� $yasyu[$i][$k]�� ���� ���� �޼�! ";
					$seiseki[3][0][$i][$k] = 1;
				}else{
					$news_kekka = "$team[$i]�� $yasyu[$i][$k]�� ����Ʈ �뷱! ";
					$seiseki[3][1][$i][$k] = 1;
				}
#			}elsif(!$tokuten[1-$i] && $total_hit[1-$i] < 4){
#				$news_kekka = "$team[$i]�� $yasyu[$i][$k]�� $total_hit[1-$i]��Ÿ �Ϻ�! ";
			}elsif(!$total_san[1-$i] > 14){
				$news_kekka = "$team[$i]�� $yasyu[$i][$k]�� $total_san[1-$i]Ż�������� �¸�! ";
			}
		}
	}else{
		$jun[$i][$k] = 9;
		$kk = 8;
	}

	$cond_plus = (20 - int(rand(40))) * 0.2;
	$cond[$i][$k] += $cond_plus;
	if($cond[$i][$k] > 9){ $cond[$i][$k] = 9; }
	if($cond[$i][$k] < 1){ $cond[$i][$k] = 1; }

	$player[$i][$kk]  = "$id[$i][$k]<>$jun[$i][$k]<>$posit[$i][$k]<>$pitch[$i][$k]<>$cond[$i][$k]<>$fas[$i][$k]<>$cha[$i][$k]<>$sei[$i][$k]<>$def[$i][$k]<>$pitwin[$i][$k]<>$pitlose[$i][$k]<>$kai[$i][$k]<>$jiseki[$i][$k]<>$san[$i][$k]<>$four[$i][$k]<>$hrp[$i][$k]";

}#end koushin_pitch

##### �� ������ ����
sub koushin_team{

	if($i eq 1 && $end_flag){
		$wincon[$i] = 0;
	}else{
		$kaio[$i] += $kai_out[$i];
		$kaid[$i] += $kai_out[1-$i];
		$get[$i]  += $seiseki[1][0][$i] = $tokuten[$i];
		$loss[$i] += $tokuten[1-$i];
		$t_jiseki[$i] += $g_jiseki[$i];
		$boxsum[$i] += $total_box[$i];
		$hitsum[$i] += $seiseki[1][1][$i] = $total_hit[$i];
		$hrsum[$i]  += $seiseki[1][2][$i] = $total_hr[$i];
		$stesum[$i] += $seiseki[1][3][$i] = $total_ste[$i];
		$errsum[$i] += $seiseki[1][5][$i] = $total_err[$i];
		$seiseki[1][4][$i] = $total_san[$i];

		$seiseki[0][1] += $seiseki[1][0][$i];
		$seiseki[0][2] += $seiseki[1][1][$i];
		$seiseki[0][3] += $seiseki[1][2][$i];
		$seiseki[0][4] += $seiseki[1][3][$i];
		$seiseki[0][5] += $seiseki[1][4][$i];
		$seiseki[0][6] += $total_four[$i];
		$seiseki[0][7] += $seiseki[1][5][$i];

		if(!$news_kekka){
			if($g_win[$i]){
				$kai = $#{$kai_ten[0]} + 1;
				if($kai > 14){
					if($i eq 1 && $sayonara){
						$news_kekka = "$team[$i]�� ����$kaiȸ ������ �������� �¸�! ";
					}else{
						$news_kekka = "$team[$i]�� ����$kaiȸ �������� �¸�! ";
					}
				}elsif($tensa2 > 14){
					$news_kekka = "$team[$i]�� $tokuten[$i]�������� �н�! ";
				}elsif($tokuten[$i] > 15 && $total_hit[$i] > 19){
					$news_kekka = "$team[$i]�� $total_hit[$i]��Ÿ $tokuten[$i]�������� �¸�! ";
				}elsif($total_hr[$i] > 4){
					$news_kekka = "$team[$i]�� $total_hr[$i]�� Ȩ��Ÿ�� �¸�! ";
				}
			}elsif($wincon[$i] > 7){
				$news_kekka = "$team[$i]�� ������ $wincon[$i]�� ����! ";
			}
		}

		$win[$i]  += $g_win[$i];
		$lose[$i] += $g_lose[$i];

		if($g_win[$i])	{ $wincon[$i]++; }
		else			{ $wincon[$i] = 0; }

		if($wincon[$i] > $winmax[$i]){
			$winmax[$i] = $wincon[$i];
		}
	}

	$teamdata[$i] = "$lastjun[$i]<>$win[$i]<>$wincon[$i]<>$winmax[$i]<>$lose[$i]<>$kaio[$i]<>$kaid[$i]<>$get[$i]<>$loss[$i]<>$t_jiseki[$i]<>$boxsum[$i]<>$hitsum[$i]<>$hrsum[$i]<>$stesum[$i]<>$errsum[$i]";

}#end koushin_team

##### ���� ���� ó��
sub game_end{

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

	@{$bumon[0]} = ('���� ����', '�ִ� ����', '�ִ� ��Ÿ', '�ִ� Ȩ��Ÿ', '�ִ� ����', '�ִ� ����', '�ִ� ����/���庼', '�ִ� ��å');
	@{$bumon[1]} = ('�ִ� ����', '�ִ� ��Ÿ', '�ִ� Ȩ��Ÿ', '�ִ� ����', '�ִ� ����', '�ִ� ��å');
	@{$bumon[2]} = ('�ִ� ��Ÿ', '�ִ� Ȩ��Ÿ', '�ִ� Ÿ��', '�ִ� ����', '�ִ� ����', '�ִ� ��å');
	@{$bumon[3]} = ('���� ����', '����Ÿ ������ ����', '�ִ�Ż����', '�ִ� ����', '�ִ���Ȩ��Ÿ', '�ִٿ�����/���庼');
	$news_record = '';
	for($i=0; $i<4; $i++){
		@kiroku = split(/<d>/, $records[$i]);
		$j = 0;
		foreach $check (@kiroku){
			if($i eq 0){
				if($seiseki[0][$j] && $seiseki[0][$j] >= (split(/<>/, $check))[0]){
					if($j eq 6)		{ $t0 = $total_four[0];			$t1 = $total_four[1]; }
					elsif($j eq 7)	{ $t0 = $seiseki[1][5][0];		$t1 = $seiseki[1][5][1]; }
					elsif($j > 0)	{ $t0 = $seiseki[1][$j-1][0];	$t1 = $seiseki[1][$j-1][1]; }
					if($j)	{ $t0 = "($t0)"; $t1 = "($t1)"; }
					else	{ $t0 = '';	$t1 = ''; }
					$check = "$seiseki[0][$j]<>$team[0]$t0, $team[1]$t1<>$saku[0], $saku[1]<>$pr_dai<>$times";
					if(!$news_record){
						if(!$j && $seiseki[0][0] > 12 || $j){
							$news_record = "���� $bumon[0][$j] ����� ����! ";
						}
					}
				}
			}else{
				for($k=0; $k<2; $k++){
					if($i eq 1){
						if($seiseki[1][$j][$k] && $seiseki[1][$j][$k] >= (split(/<>/, $check))[0]){
							$check = "$seiseki[1][$j][$k]<>$team[$k]<>$saku[$k]<>$pr_dai<>$times";
							if(!$news_record){
								$news_record = "$team[$k]�� �� $bumon[1][$j] ����� ����! ";
							}
						}
					}else{
						if($i eq 2){
							for($h=0; $h<8; $h++){
								if($seiseki[2][$j][$k][$h] && $seiseki[2][$j][$k][$h] >= (split(/<>/, $check))[0]){
									$check = "$seiseki[2][$j][$k][$h]<>$yasyu[$k][$h]<>$team[$k]<>$pr_dai<>$times";
									if(!$news_record){
										$news_record = "$team[$k]�� $yasyu[$k][$h]�� $bumon[2][$j] ����� ����! ";
									}
								}
							}
						}else{
							if(($j eq 0 || $j eq 1) && $seiseki[3][$j][$k][8]){
								$check = "-<>$pitch[$k][8]<>$team[$k]<>$pr_dai<>$times";
							}elsif($seiseki[3][$j][$k][8] && $seiseki[3][$j][$k][8] >= (split(/<>/, $check))[0]){
								$check = "$seiseki[3][$j][$k][8]<>$pitch[$k][8]<>$team[$k]<>$pr_dai<>$times";
								if(!$news_record){
									$news_record = "$team[$k]�� $pitch[$k][8]�� $bumon[3][$j] ����� ����! ";
								}
							}
						}
					}
				}
			}
			$j++;
		}
		$records[$i] = join('<d>', @kiroku);
	}

	truncate (RC, 0);
	seek(RC,0,0);	print RC @records;
	close(RC);
	eval 'flock(RC,8);';

# ���� ���Ͽ��� ������
	open(US,"+<$leaguefold/$userfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(US,2);';

	@users = <US>;

	$c_flag = $w_flag = 0;
	foreach(@users){
		($checksaku,$checkpass,$d,$d,$d,$checktime,$d,$checkteamdata) = split /<p>/;
		($d,$checkwin,$d,$d,$checklose) = split(/<>/, $checkteamdata);
		if($checkpass eq $pass[0] && $checksaku eq $saku[0]){
			if($c_flag){ $_ = ''; }
			else{ $_ = $userdata[0]; $c_flag = 1; }
		}elsif($checkpass eq $pass[1] && $checksaku eq $saku[1]){
			if($w_flag){ $_ = ''; }
			else{ $_ = $userdata[1]; $w_flag = 1; }
		}elsif(	($times > ($checktime + $userlimit * 24 * 60 * 60) || $checksaku eq '')
				||
				($times > ($checktime + $nogamelimit * 24 * 60 * 60) && ($checkwin + $checklose) eq 0)
		){
			$_ = '';
		}
	}

	&team_sort1;

	@users = (@winranks, @else_teams);

	truncate (US, 0); 
	seek(US,0,0);	print US @users;
	close(US);
	eval 'flock(US,8);';

# ���� ������ ���Ͽ��� ������
	open(YD,"$leaguefold/$yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(YD,1);';
	seek(YD,0,0);  @yasyus = <YD>;  close(YD);
	eval 'flock(YD,8);';

	open(PD,"$leaguefold/$pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(PD,1);';
	seek(PD,0,0);  @pitchs = <PD>;  close(PD);
	eval 'flock(PD,8);';

	for($k=0; $k<10; $k++){
		($id[0]) = split(/<>/,$player[0][$k]);
		($id[1]) = split(/<>/,$player[1][$k]);
		$c_play_flag = 0;
		$w_play_flag = 0;
		$c_play_kakiko = "$team[0]<>$times<>$player[0][$k]<>\n";
		$w_play_kakiko = "$team[1]<>$times<>$player[1][$k]<>\n";
		if($k < 8)	{ @lines = @yasyus; }
		else		{ @lines = @pitchs; }
		foreach(@lines){
			($checkteam,$checktime,$checkid,$dmy,$dmy,$checkname) = split /<>/;
			if($checkteam eq $team[0] && $checkid eq $id[0]){
				$_ = $c_play_kakiko;
				$c_play_flag = 1;
			}elsif($checkteam eq $team[1] && $checkid eq $id[1]){
				$_ = $w_play_kakiko;
				$w_play_flag = 1;
			}elsif($times > ($checktime + $userlimit * 24 * 60 * 60) || $checkteam eq ''){ $_ = ''; }
		}
		if(!$c_play_flag){	push (@lines, $c_play_kakiko); }
		if(!$w_play_flag){	push (@lines, $w_play_kakiko); }
		if($k < 8)	{ @yasyus = @lines; }
		else		{ @pitchs = @lines; }
	}
	open(YD,"+<$leaguefold/$yasyufile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(YD,2);';
	truncate (YD, 0); 
	seek(YD,0,0);	print YD @yasyus;
	close(YD);
	eval 'flock(YD,8);';

	open(PD,"+<$leaguefold/$pitchfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(PD,2);';
	truncate (PD, 0); 
	seek(PD,0,0);	print PD @pitchs;
	close(PD);
	eval 'flock(PD,8);';

# ������ �¸��� ���Ͽ��� ������
	if($tensa2 > 0 || $end_flag){
		$winner = $userdata[0];
	}else{
		$winner = $userdata[1];
	}

	open(WN,"+<$leaguefold/$winfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(WN,2);';
	truncate (WN, 0); 
	seek(WN,0,0);	print WN $winner;
	close(WN);
	eval 'flock(WN,8);';

# ������ ��� ���Ͽ��� ������
	open(LG,"+<$leaguefold/$logfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(LG,2);';

	@g_log = <LG>;
	$k_log = "$times<>$team[0] $tokuten[0]-$tokuten[1] $team[1]<>@log<>\n";
	unshift(@g_log,$k_log);
	splice(@g_log,5);

	for($i=3; $i<5; $i++){
		($g_date, $g_kekka) = split(/<>/, $g_log[$i]);
		$g_log[$i] = "$g_date<>$g_kekka<>\n";
	}

	truncate (LG, 0); 
	seek(LG,0,0);	print LG @g_log;
	close(LG);
	eval 'flock(LG,8);';

# �ڸ�Ʈ ���� ����
	if($geki_news && ($news_kekka || $news_record)){
		open(CF,"+<$commentfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
		eval 'flock(CF,2);';

		@comments = <CF>;
		if($news_record){ $news_kekka = $news_record; }
		$kakiko = "1<><><>$times<>$news_kekka<>$team[0] $tokuten[0] - $tokuten[1] $team[1]<>\n";

		unshift(@comments, $kakiko);
		splice(@comments, $com_max);

		truncate (CF, 0); 
		seek(CF,0,0);	print CF @comments;
		close(CF);
		eval 'flock(CF,8);';
	}

# �� ����
	$gamelock = "0<>$times<>\n";

	open(GL,"+<$leaguefold/$lockfile") || &error('������ ������ ������ �ʽ��ϴ�. ');
	eval 'flock(GL,2);';
	truncate (GL, 0);
	seek(GL,0,0);	print GL $gamelock;
	close(GL);
	eval 'flock(GL,8);';

}#end game_end

1;
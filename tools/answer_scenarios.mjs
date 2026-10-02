// 공개문제 동작 사항을 옮긴 시험 순서 (tools/check_answers.mjs가 쓴다. 타이머 2초, 플리커 4초). 'MC1'은 켜짐, 'MC1-'은 꺼짐을 확인한다.
export default {
1: `ss A; lvl 2; X MC1 RL M1 T- MC2-; lvl 0; X- MC1- M1-; ss M; pb PB1; T MC1 RL M1 MC2-; wait 2.2; MC2 GL M2; pb PB0; T- MC1- MC2- RL- GL-;
    pb PB1; trip; MC1- M1- FR BZ YL-; wait 4.1; BZ- YL; reset; FR- BZ- YL- MC1-`,
2: `ss A; lvl 2; X T MC1-; wait 2.2; FR MC1 RL M1 MC2-; wait 4.1; MC1- MC2 GL M2; lvl 0; X- T- FR- MC1- MC2-;
    ss M; pb PB1; X T; wait 2.2; FR MC1; pb PB0; X- T- MC1-; pb PB1; wait 2.2; trip; MC1- MC2- BZ YL; reset; BZ- YL- X-`,
3: `ss A; lvl 2; FR MC1 RL M1; wait 4.1; MC1- MC2 GL; lvl 0; FR- MC1- MC2-; ss M; pb PB1; T X-; wait 2.2; X FR MC1 RL;
    pb PB0; T- X- FR- MC1-; trip; BZ YL; reset; BZ- YL-`,
4: `ss A; lvl 2; X FR MC1 RL M1 MC2- T-; wait 4.1; MC1- MC2 T GL; wait 2.2; MC2- MC1- GL- RL-; wait 2.0; MC1 RL; lvl 0; X- FR- MC1-;
    ss M; pb PB1; X FR MC1; pb PB0; X- MC1-; trip; BZ YL`,
5: `ss A; lvl 2; T X FR MC1 MC2-; wait 2.2; FR- MC1 MC2 RL GL M1 M2; lvl 0; T- X- MC1- MC2-; ss M; pb PB1; T X FR MC1 MC2-;
    wait 2.2; FR- MC1 MC2; pb PB0; MC1- MC2- T-; trip; BZ YL`,
6: `ss A; lvl 2; X MC1 MC2 RL GL M1 M2 T-; lvl 0; X- MC1- MC2-; ss M; pb PB1; T MC1 MC2; wait 2.2; MC2- FR MC1; wait 4.1; MC1- MC2;
    pb PB0; T- FR- MC1- MC2-; trip; BZ YL`,
7: `ss A; lvl 2; X FR T MC1 RL M1 MC2-; wait 2.2; MC1- MC2 GL M2; wait 2.0; MC1- MC2- GL- RL-; wait 4.0; MC1 RL T; lvl 0; X- FR- MC1-;
    ss M; pb PB1; X FR T MC1; pb PB0; X- MC1-; trip; BZ YL`,
8: `ss A; lvl 2; FR X MC1 MC2 RL GL YL M1 M2; wait 4.1; YL-; wait 4.0; YL; lvl 0; FR- X- MC1- MC2- YL-; ss M; pb PB1; T MC1 MC2 RL GL;
    wait 2.2; MC1- MC2- RL- GL- T; pb PB0; T-; pb PB1; trip; MC1- MC2- BZ`,
9: `ss A; lvl 2; MC1 RL M1 X-; lvl 0; MC1-; ss M; pb PB1; X T MC1 RL; wait 2.2; MC2 GL M2; pb PB0; X- T- MC1- MC2-;
    pb PB1; trip; MC1- FR BZ YL-; wait 4.1; BZ- YL; reset; FR- BZ- YL-`,
10: `pb PB1; X1 WL T1-; ls1 1; T1; wait 2.2; MC1 RL WL- M1; ls1 0; T1- MC1- RL- WL; pb PB2; X2; ls2 1; T2; wait 2.2; MC2 GL M2;
    pb PB0; X1- X2- T2- MC2- WL-; pb PB1; ls1 1; wait 2.2; trip; MC1- M1- YL; reset; YL- X1-`,
11: `pb PB1; X1- T1-; hold PB1; X1 T1 WL; wait 2.2; release PB1; X1 T1 WL; ls1 1; MC1 RL M1 WL-; ls1 0; MC1- WL;
    hold PB2; X2 T2 X1- T1-; wait 2.2; release PB2; X2 T2; ls2 1; MC2 GL M2 WL-; pb PB0; X2- T2- MC2- GL-; trip; YL; reset; YL-`,
12: `pb PB1; X1 T1 WL; ls1 1; MC1 T1- RL M1 WL-; ls1 0; T1 MC1- WL; wait 2.2; X2 MC2 GL M2; pb PB0; X1- X2- T1- MC2- WL-;
    pb PB2; X2 MC2 GL; ls2 1; T2 WL; wait 2.2; X1 T1; ls1 1; MC1 T1- RL; pb PB0; X1- X2- MC1- MC2-`,
13: `pb PB1; X1 T1 WL; ls2 1; MC1 T1- RL M1 WL-; ls2 0; T1 MC1- WL; wait 2.2; X2 T2 MC2 GL M2; wait 2.2; X1- T1- T2- WL- MC2;
    pb PB0; X2- MC2-; ls1 1; X1 T1; ls1 0; X1 T1; pb PB0; X1-; pb PB1; ls2 1; MC1; pb PB2; X2 MC2 WL`,
14: `ls1 1; ls2 1; X1 X2 WL; pb PB1; T1 MC1 RL M1 WL-; wait 2.2; T1- MC1- RL- WL; pb PB1; MC1; ls2 0; MC1- T1- WL;
    pb PB2; T2 MC2 GL WL-; wait 2.2; T2- MC2- WL; pb PB2; MC2; ls1 0; MC2- T2-; ls1 1; ls2 1; pb PB2; MC2 T2`,
15: `ls1 1; pb PB1; T1 MC1 RL WL-; ls1 0; MC1 T1; wait 2.2; T1- MC1- WL; pb PB2; MC2-; ls1 1; ls2 1; pb PB2; T2 MC2 GL WL-;
    ls1 0; ls2 0; MC2; wait 2.2; MC2- T2-`,
16: `ls1 1; T1 X1-; wait 2.2; X1 MC1 RL M1; ls1 0; MC1 T1-; pb PB0; X1- MC1-; pb PB1; X1 MC1; pb PB2; X2-; ls1 1; pb PB2; X2 MC2 GL M2;
    pb PB0; ls2 1; T2 X2 MC2 GL; wait 2.2; MC2- GL- WL; ls2 0; MC2 GL WL-`,
17: `ls1 1; pb PB1; T1 MC1 RL M1; ls2 1; T1- MC1-; ls2 0; pb PB1; MC1; pb PB2; MC2-; wait 2.2; pb PB2; T2 MC2 GL M2;
    wait 2.2; MC2- WL; pb PB0; T1- MC1- T2- WL-; ls1 0; pb PB1; MC1-`,
18: `ls1 1; pb PB1; T1 MC1 RL M1 WL-; wait 2.2; WL; ls1 0; ls2 1; MC1; pb PB0; MC1- WL-; pb PB2; T2 MC2 GL; wait 2.2; WL;
    pb PB0; T2- MC2-; ls2 0; pb PB2; MC2-`,
};

# 회로도 맨 아래 줄 부하(코일·램프·부저)의 왼쪽→오른쪽 순서 (그림에서 읽음)
LOADS = {
1: 'EOCR FR YL BZ FLS X T MC1 MC2 RL GL', 2: 'EOCR YL BZ FLS X T FR MC1 MC2 RL GL', 3: 'EOCR YL BZ MC1 MC2 FR FLS T X RL GL',
4: 'EOCR YL BZ FLS FR X MC1 MC2 T RL GL', 5: 'EOCR YL BZ FLS X T FR MC1 MC2 RL GL', 6: 'EOCR YL BZ FLS X T FR MC1 RL GL MC2',
7: 'EOCR YL BZ FLS FR X T MC1 MC2 RL GL', 8: 'EOCR BZ FLS X FR YL T MC1 MC2 RL GL', 9: 'EOCR FR YL BZ MC1 FLS X T MC2 RL GL',
10: 'EOCR YL X1 T1 MC1 X2 T2 MC2 WL RL GL', 11: 'EOCR YL X1 MC1 T1 X2 MC2 T2 WL RL GL', 12: 'EOCR YL X1 MC1 T1 X2 MC2 T2 WL RL GL',
13: 'EOCR YL X1 MC1 T1 X2 MC2 T2 WL RL GL', 14: 'EOCR YL X1 X2 MC1 T1 RL MC2 T2 GL WL', 15: 'EOCR YL X1 X2 MC1 T1 RL MC2 T2 GL WL',
16: 'EOCR YL T1 T2 MC1 X1 RL MC2 WL X2 GL', 17: 'EOCR YL X1 X2 MC1 T1 RL MC2 WL T2 GL', 18: 'EOCR YL X1 X2 MC1 T1 RL MC2 T2 GL WL'}
# 접점 중 구조로 구별되지 않는 것: (왼쪽 것, 오른쪽 것) — x 위치로 가른다
LEFT = {
5: [('FR.fa', 'T.ta')], 6: [('T.tb', 'FR.fa')],
11: [('PB1.a', 'T1.ta'), ('PB2.a', 'T2.ta')],
12: [('PB1.a', 'X1.a'), ('X1.a', 'T2.ta'), ('PB2.a', 'X2.a'), ('X2.a', 'T1.ta'), ('T1.ia', 'T2.ia')],
13: [('PB1.a', 'X1.a#1'), ('X1.a#1', 'TB4.ls1'), ('PB2.a', 'X2.a'), ('X2.a', 'T1.ta'), ('T1.ia', 'T2.ia')],
14: [('X1.a#2', 'X2.a#2')], 15: [('X1.a#1', 'X2.a#1')],
16: [('PB1.a', 'X1.a'), ('X1.a', 'T1.ta'), ('PB2.a', 'X2.a'), ('X2.a', 'T2.ia')],
17: [('X1.a', 'X1.b'), ('X2.b', 'X2.a')], 18: [('T1.ta', 'T2.ta')]}

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('Malgun', 'C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold', 'C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFont(TTFont('MalgunItalic', 'C:/Windows/Fonts/malgunsl.ttf'))
pdfmetrics.registerFontFamily('Malgun', normal='Malgun', bold='MalgunBold', italic='MalgunItalic', boldItalic='MalgunBold')

doc = SimpleDocTemplate(
    "C:/Users/a9144/Projects/computer/unity_code_explanation.pdf",
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=20*mm, bottomMargin=20*mm
)

T  = ParagraphStyle('T',  fontName='MalgunBold', fontSize=18, leading=26, spaceAfter=4)
H  = ParagraphStyle('H',  fontName='MalgunBold', fontSize=13, leading=20, spaceBefore=8, spaceAfter=4)
H2 = ParagraphStyle('H2', fontName='MalgunBold', fontSize=11, leading=18, spaceBefore=6, spaceAfter=2)
CD = ParagraphStyle('CD', fontName='Malgun',     fontSize=10, leading=16, backColor='#eeeeee', leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=2)
BL = ParagraphStyle('BL', fontName='Malgun',     fontSize=11, leading=18, leftIndent=16)
NM = ParagraphStyle('NM', fontName='Malgun',     fontSize=11, leading=18)

def sec(title):
    return [HRFlowable(width="100%", thickness=1, color='#cccccc', spaceAfter=4),
            Paragraph(title, H)]

def row(code, items):
    out = [Paragraph(code, CD)]
    for i in items:
        out.append(Paragraph("• " + i, BL))
    out.append(Spacer(1, 3*mm))
    return out

content = []

content.append(Paragraph("Unity 스크립트 코드 설명서 v2", T))
content.append(Paragraph("playermove · camerafollow · enemymove · allyhealth", NM))
content.append(Spacer(1, 3*mm))

content.append(Paragraph("<b>표기 규칙</b>", H2))
content.append(Paragraph("• <b>굵게</b>  =  고정 문법 (바꾸면 안 됨)", BL))
content.append(Paragraph("• <i>기울임</i>  =  내가 붙인 이름 (바꿔도 됨)", BL))
content.append(Paragraph("• 회색 배경  =  Unity 제공 기능", BL))
content.append(Spacer(1, 5*mm))

# ── 1. playermove ──
content += sec("1. playermove.cs  —  플레이어 이동 + 점프")

content.append(Paragraph("<b>변수 선언</b>", H2))
content += row("public float speed = 5f;", [
    "<b>public</b> = Unity Inspector에서 보이고 수정 가능 / <b>float</b> = 소수점 숫자 타입",
    "<i>speed</i> = 캐릭터의 이동 속도를 조절하기 위한 변수. Inspector에서 바꾸면 즉시 반영됨",
    "= 5f = 기본값 5 (f는 float 타입임을 표시)",
])
content += row("public float jumpForce = 1f;", [
    "<i>jumpForce</i> = 점프할 때 위로 가하는 힘의 세기를 조절하기 위한 변수",
    "= 1f = 기본값 1. Inspector에서 높이면 더 높이 점프함",
])
content += row("private Rigidbody2D rb;", [
    "<b>private</b> = Inspector에 안 보임, 코드 내부에서만 사용",
    "Rigidbody2D = Unity 물리 컴포넌트 타입 (중력, 힘 등을 처리)",
    "<i>rb</i> = 점프할 때 AddForce를 호출하려고 물리 컴포넌트를 미리 담아두는 변수",
])
content += row("private bool isGrounded = false;", [
    "<b>bool</b> = true / false 두 값만 가질 수 있는 타입",
    "<i>isGrounded</i> = 플레이어가 지금 땅에 닿아 있는지 기억하기 위한 변수",
    "= false = 게임 시작 시 땅에 없다고 가정. 바닥에 닿으면 true로 바뀜",
    "이 값이 false면 공중이므로 점프를 막아 공중점프 방지",
])

content.append(Paragraph("<b>Start()</b>  —  게임 시작 시 딱 한 번 실행", H2))
content += row("rb = GetComponent<Rigidbody2D>();", [
    "GetComponent<Rigidbody2D>() = 이 오브젝트에 붙은 Rigidbody2D를 찾는 Unity 함수",
    "<i>rb</i>에 저장해둬야 Update()에서 점프할 때 사용 가능",
])

content.append(Paragraph("<b>Update()</b>  —  매 프레임(1초에 약 60번) 실행", H2))
content += row("Vector2 input = Vector2.zero;", [
    "Vector2 = x, y 두 값을 가지는 Unity 타입 (방향 표현에 사용)",
    "<i>input</i> = 이번 프레임에 플레이어가 어느 방향으로 움직일지 저장하는 변수",
    "Vector2.zero = (0, 0) 즉 아무 방향도 아님 = 정지 상태로 초기화",
])
content += row("if (Keyboard.current.leftArrowKey.isPressed) input.x = -1;", [
    "Keyboard.current = 현재 키보드 상태",
    "isPressed = 키를 누르고 있는 동안 계속 true",
    "<i>input.x</i> = -1 = 왼쪽 방향으로 이동하도록 설정",
])
content += row("transform.position += new Vector3(input.x, 0, 0) * speed * Time.deltaTime;", [
    "transform.position = 오브젝트의 현재 위치",
    "+= = 현재 위치에 더해서 이동",
    "new Vector3(input.x, 0, 0) = x 방향으로만 이동 (y, z는 0으로 고정)",
    "<i>speed</i> = 이동 거리에 속도를 곱해서 빠르기 조절",
    "Time.deltaTime = 컴퓨터 성능에 상관없이 항상 같은 속도로 이동하게 해줌",
])
content += row("if (Keyboard.current.spaceKey.wasPressedThisFrame && isGrounded)", [
    "wasPressedThisFrame = 이번 프레임에 처음 누른 순간만 true (꾹 누르기 제외)",
    "&& = 그리고. 스페이스 누른 순간 AND 땅에 있을 때만 점프 실행",
    "<i>isGrounded</i>가 false면 공중이므로 점프 불가",
])
content += row("rb.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);", [
    "AddForce = 물리 엔진에 힘을 가하는 Unity 함수",
    "Vector2.up = 위쪽 방향 (0, 1)",
    "<i>jumpForce</i> = 점프 세기. Inspector에서 조절 가능",
    "ForceMode2D.Impulse = 순간적으로 강하게 힘을 줌 (튕기는 느낌)",
])
content += row("isGrounded = false;", [
    "점프 직후 공중 상태로 바꿔서 연속 점프(공중점프) 방지",
])

content.append(Paragraph("<b>OnCollisionEnter2D()</b>  —  다른 오브젝트에 닿는 순간 자동 실행", H2))
content += row("isGrounded = true;", [
    "바닥(또는 어떤 물체)에 닿으면 <i>isGrounded</i>를 true로 바꿔서 다시 점프 가능하게 함",
])

content.append(Spacer(1, 5*mm))

# ── 2. camerafollow ──
content += sec("2. camerafollow.cs  —  카메라가 캐릭터를 부드럽게 따라가기")

content.append(Paragraph("<b>변수 선언</b>", H2))
content += row("public Transform target;", [
    "Transform = 오브젝트의 위치·회전·크기 정보를 담는 Unity 타입",
    "<i>target</i> = 카메라가 따라갈 대상을 저장하는 변수. Inspector에서 캐릭터를 드래그해서 연결",
])
content += row("public float smoothSpeed = 5f;", [
    "<i>smoothSpeed</i> = 카메라가 목표 위치로 얼마나 빠르게 따라갈지 조절하는 변수",
    "값이 클수록 빠르게 따라가고, 작을수록 천천히 따라감",
])

content.append(Paragraph("<b>LateUpdate()</b>  —  모든 Update() 실행 후 마지막에 실행", H2))
content += row("if (target == null) return;", [
    "<i>target</i>이 Inspector에서 연결 안 됐으면 오류 없이 그냥 종료",
])
content += row("Vector3 goal = new Vector3(target.position.x, target.position.y, transform.position.z);", [
    "<i>goal</i> = 카메라가 이동해야 할 목표 위치를 계산해서 저장하는 변수",
    "target.position.x / .y = 캐릭터의 x, y 위치를 따라감",
    "transform.position.z = 카메라의 z(깊이)는 건드리지 않고 그대로 유지",
])
content += row("transform.position = Vector3.Lerp(transform.position, goal, smoothSpeed * Time.deltaTime);", [
    "Vector3.Lerp = 두 위치 사이를 부드럽게 보간하는 Unity 함수",
    "현재 위치에서 <i>goal</i> 쪽으로 조금씩 이동 → 뚝뚝 끊기지 않고 부드러운 카메라 효과",
])

content.append(Spacer(1, 5*mm))

# ── 3. enemymove ──
content += sec("3. enemymove.cs  —  적 캐릭터 좌우 왕복 이동")

content.append(Paragraph("<b>변수 선언</b>", H2))
content += row("public float speed = 2f;", [
    "<i>speed</i> = 적이 얼마나 빠르게 이동할지 조절하는 변수",
])
content += row("public float range = 3f;", [
    "<i>range</i> = 시작 위치에서 좌우로 얼마나 멀리 이동할지 범위를 저장하는 변수",
    "= 3f = 시작 위치 기준 왼쪽 3, 오른쪽 3 범위 내에서 왕복",
])
content += row("private Vector3 startPos;", [
    "<i>startPos</i> = 게임 시작 시 적의 위치를 기억해두는 변수",
    "왕복 범위를 계산할 때 기준점으로 사용 (이 값이 없으면 범위를 알 수 없음)",
])
content += row("private int dir = 1;", [
    "<b>int</b> = 정수 타입 (소수점 없음)",
    "<i>dir</i> = 현재 이동 방향을 저장하는 변수. 1 = 오른쪽, -1 = 왼쪽",
    "= 1 = 처음엔 오른쪽으로 출발",
])

content.append(Paragraph("<b>Start()</b>", H2))
content += row("startPos = transform.position;", [
    "게임 시작 시 현재 위치를 <i>startPos</i>에 저장해서 왕복 기준점으로 사용",
])

content.append(Paragraph("<b>Update()</b>", H2))
content += row("transform.position += new Vector3(speed * dir * Time.deltaTime, 0, 0);", [
    "<i>speed</i> × <i>dir</i> = 속도 × 방향. dir이 -1이면 왼쪽으로 이동",
    "매 프레임 조금씩 이동해서 부드러운 움직임 만들기",
])
content += row("if (transform.position.x > startPos.x + range) dir = -1;", [
    "오른쪽 한계(시작점 + range)에 도달하면 <i>dir</i>을 -1로 바꿔서 왼쪽으로 전환",
])
content += row("if (transform.position.x < startPos.x - range) dir = 1;", [
    "왼쪽 한계(시작점 - range)에 도달하면 <i>dir</i>을 1로 바꿔서 오른쪽으로 전환",
])

content.append(Spacer(1, 5*mm))

# ── 4. allyhealth ──
content += sec("4. allyhealth.cs (PlayerHealth)  —  플레이어 HP 시스템")

content.append(Paragraph("<b>변수 선언</b>", H2))
content += row("public int maxHp = 3;", [
    "<b>int</b> = 정수 타입",
    "<i>maxHp</i> = 플레이어의 최대 HP를 저장하는 변수. Inspector에서 바꿀 수 있음",
    "= 3 = 기본값 3칸",
])
content += row("private int hp;", [
    "<i>hp</i> = 현재 HP를 실시간으로 추적하는 변수. 피격 시 1씩 감소",
    "Start()에서 maxHp 값으로 초기화됨",
])
content += row("private float invincibleTime = 1.5f;", [
    "<i>invincibleTime</i> = 피격 후 무적 시간을 저장하는 변수",
    "= 1.5f = 한 번 맞으면 1.5초 동안 다시 안 맞음. 연속 데미지 방지용",
])
content += row("private float lastHitTime = -10f;", [
    "<i>lastHitTime</i> = 마지막으로 피격당한 시간을 기록하는 변수",
    "= -10f = 게임 시작하자마자 맞을 수 있도록 충분히 작은 값으로 초기화",
    "Time.time(현재 시간) - lastHitTime이 1.5초 넘어야 다시 피격 가능",
])

content.append(Paragraph("<b>Start()</b>", H2))
content += row("hp = maxHp;", [
    "게임 시작 시 현재 HP를 최대값으로 설정",
])

content.append(Paragraph("<b>OnCollisionEnter2D()</b>  —  다른 오브젝트에 닿는 순간 실행", H2))
content += row("if (col.gameObject.GetComponent<EnemyMove>() == null) return;", [
    "닿은 오브젝트에 EnemyMove 스크립트가 없으면 무시",
    "바닥, 벽 등에 닿아도 HP가 안 깎히도록 적만 필터링",
])
content += row("if (Time.time - lastHitTime < invincibleTime) return;", [
    "Time.time = 게임 시작 후 경과 시간(초)",
    "마지막 피격 후 1.5초가 안 지났으면 무시 → 무적 시간 구현",
])
content += row("lastHitTime = Time.time;", [
    "지금 시간을 <i>lastHitTime</i>에 저장해서 다음 피격 가능 시간 계산에 사용",
])
content += row("hp--;", [
    "-- = 1 감소. hp = hp - 1 과 동일",
    "현재 HP를 1 깎음",
])
content += row('Debug.Log($"HP: {hp}/{maxHp}");', [
    "Debug.Log = Unity Console 창에 메시지를 출력하는 개발용 함수",
    '$"..." = 문자열 안에 변수 값을 직접 넣는 방법. {hp}는 현재 HP 값으로 치환됨',
])
content += row("if (hp <= 0) SceneManager.LoadScene(GetActiveScene().name);", [
    "HP가 0 이하가 되면 현재 씬을 다시 로드 → 게임 재시작",
    "GetActiveScene().name = 현재 씬 이름을 가져옴",
    "LoadScene = 해당 이름의 씬을 새로 불러오는 Unity 함수",
])

doc.build(content)
print("PDF 저장 완료")

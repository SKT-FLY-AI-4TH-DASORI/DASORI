# DASORI
Project Dasori: SKT FLY AI 4기 Ziller DaSori 서비스 프로젝트입니다.

**팀원: 문정현, 김다은, 이가경, 강예람, 최재훈**

## **GitHub 협업 공지사항**

### 1. **Organization에 있는 repository “Fork”하기**

### 2. **자신의 github repository에 제대로 복사됐는지 확인 후, local에 git clone하기**
`git clone [repository 주소]`

### 3. **프로젝트 열기**

### 4. Organization repository 추가 및 확인하기
- **repository 추가** </br>
    `git remote add upstream [organization 주소]`
    
- **repository 확인** </br>
    `git remote -v` </br>
      ❗fork한 내 repository는 **origin**, organization의 repository는 **upstream**

### 5.  **기능에 맞는 자신만의 작업 공간인 branch 생성**

**❗항상 우선적으로 `git branch`로 브랜치 확인❗**
 
**Branch 사용법**

1. 브랜치 생성 </br>
    `git branch 타입/기능`
    - `타입/`  후 띄어쓰기 없이 작성
    - 타입: 첫글자만 대문자로 작성
    - 기능: 첫글자는 대문자로, 기능 이름으로 작성
      
2. 브랜치 생성 확인 </br>
    `git branch`
    
3. 브랜치 이동 </br>
    `git checkout 타입/기능`
    
4. 코드 작성
5. add, commit 등 수행

**Branch 이름 포멧**

| 타입 | 설명 | 예시 |
| --- | --- | --- |
| Feat | 새로운 기능 구현 | Feat/Login |
| Refactor | 기능 수정  | Refactor/Login |

### 6. 자신 브랜치에서 작업 후 add, commit, push, pull & request

**❗항상 우선적으로 `git branch`로 브랜치 확인❗**

**Commit & PR 사용법**

1. `git pull` 하기
2. `git branch 브랜치명`으로 내가 작업할 브랜치로 이동
3. 코드 수정
4. `git add .` → `git commit -m “타입: 설명”`
    - `타입:` 후 띄어쓰기 필수
    - 타입: 모두 대문자
    - 설명: 영어일 경우, 첫 글자만 대문자
        - 간단히 작성
  
5. `git push origin 자신 브랜치`

6. push 이후, 자신의 github repository 확인 
    작업했던 branch로 이동→ **compare & pull request** 클릭

7. Pull Request 메세지 작성
    - 줄바꿈 필수
    - 설명 최대한 상세하게 작성
    - Issue 번호가 없다면 생략 가능
    
8. 이러면 끝인데, **Merge pull request는 절대 하지 말것** 
    - 현재까지 작업: **upstream -> (fork) -> origin -> (add/commit/push) -> pull&request -> upstream(merge) 요청**
    
9. 변경(merge)된 upstream을 현재 내가 작업하고 있던 fork한 origin 저장소에 반영해야함 </br>
    `git branch` → `git checkout main` → `git fetch upstream` → `git merge upstream/main` → `git push origin main`

**Commit 메세지 포멧**

| 타입 | 설명 | 예시 |
| --- | --- | --- |
| FEAT (추가) | 새로운 기능 구현 | FEAT: 로그인 로직 기능 추가 |
| REFACTOR | 내부 로직은 변경하지 않고 코드 개선 및 삭제 | REFACTOR: 코드 줄바꿈 수정 |
| FIX | 버그 또는 오류 해결 | FIX: 로그인 로직 오류 해결 |
| CHORE | 빌드 관련 작업 (버전 코드 수정, 패키지 구조 변경, 파일 이동 등) | CHORE 불필요한 패키지 삭제 |
| COMMENT | 필요한 주석 추가 또는 변경 | COMMENT: 로그인 로직 부분 주석 추가 |
| TEST | 테스트 코드 추가 및 수정 | TEST: 로그인 토큰 테스트 코드 추가 |
| STYLE | 코드 스타일 혹은 포맷 관한 수정 | STYLE: 로그인 글씨체 수정 |
| DESIGN | 화면 디자인 수정 | DESIGN: 로그인 화면 UI 수정 |
| REMOVE | 파일 삭제 | REMOVE: 중복 파일 삭제 |

**PR 메세지 포멧**

```python
# commit 메세지와 동일하게 복붙

설명 - 최대한 상세하게 작성

Issue #이슈숫자
```

---

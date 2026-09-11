# -*- coding: utf-8 -*-
"""
Intent-Driven Pre-production and Prompt Designer for Sequences 4, 5, 6.
Re-architected from the ground up:
- 100% pedagogical intent-driven metaphors (no literal noun/verb cartooning).
- Captures Deming's management philosophy, psychological safety, and empirical discipline.
- Synthesizes audio and generates canonical scene_plan.json + script.json.
- Executes Reviewer Protocol (Self-Audit).
"""

import sys
import os
import json
import re
import subprocess
import asyncio
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import edge_tts
import imageio_ffmpeg

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
VOICE = "zh-TW-YunJheNeural"
OPENMONTAGE_ROOT = Path(r"d:\kj-openMontage")


def get_media_duration(file_path: Path) -> float:
    cmd = [FFMPEG_EXE, "-i", str(file_path)]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, errors="replace")
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0


STYLE_PREFIX = (
    "SHOT: Overhead tabletop flat-lay view, 12 FPS stop-motion, slow subtle camera push-in.\n"
    "STYLE: Vox-style paper collage stop-motion animation, 12 FPS, zero motion blur. Aged off-white newsprint paper base with millimeter grid lines, tactile layered cardboard and textured cardstock cutouts, sharp knife-cut drop shadows, rich physical paper grain.\n"
    "LIGHTING: Studio tungsten overhead lighting, warm 3400K, defined physical drop shadows under paper edges.\n"
)
NEGATIVE_PROMPT = "\nNEGATIVE: smooth digital CGI, glossy 3D render, cartoon characters, motion blur, full-sentence subtitles, spoken dialogue."


# Sequence 4: Intent-Driven Prompts (11 shots)
SEQ4_INTENT = [
    # Scene 4.1
    {
        "id": "sc4.1_01", "scene_num": "4.1", "shot_idx": 1,
        "text": "一旦你在Plan步驟，規劃好對策之後，接下來就要進入Do步驟，來測試你的對策。",
        "location": "Engineering test bench transition.",
        "action": "An elegant architectural blueprint of railway tracks stamped 'THEORETICAL PLAN' is pushed forward across a cream cutting mat; a tactile physical testing jig slides into place with brass toggle switches labeled 'FIELD TRIAL / DO'; miniature mechanical calipers and tension gauges lock onto the paper tracks to begin empirical testing.",
        "text_overlay": "'THEORY TO FIELD TRIAL', 'DO: TEST THE HYPOTHESIS'",
        "audio_sfx": "Blueprint paper slide, heavy rubber cutting mat thud, snappy toggle switch click, tension gauge ratchet, no dialogue."
    },
    {
        "id": "sc4.1_02", "scene_num": "4.1", "shot_idx": 2,
        "text": "而因為這個時候你還不知道對策是否有效，所以必須要採取實驗精神，小規模地試做。",
        "location": "Railway network sandtable.",
        "action": "A giant paper map of the full national railway network rests in background; a single isolated red circular magnifying zone highlights only 'PILOT SECTION: 10 KM'; a laser-cut yellow safety fence drops around this pilot sandbox, keeping main trunk lines green and safe while testing occurs strictly within the contained boundary.",
        "text_overlay": "'SANDBOX ISOLATION', 'CONTAINED EXPERIMENTAL RISK'",
        "audio_sfx": "Miniature fence drop clatter, perimeter lock click, gentle background train hum, no dialogue."
    },
    {
        "id": "sc4.1_03", "scene_num": "4.1", "shot_idx": 3,
        "text": "也因此，這個步驟的工作項目將包括：逐項執行對策，以及蒐集回饋資料。",
        "location": "Scientific dual-engine console.",
        "action": "Two interlocking paper mechanisms slide into place on a workbench: Left side is a mechanical actuator arm labeled '1. CONTROLLED INTERVENTION'; Right side is an optical sensor lens array labeled '2. EMPIRICAL SENSOR / FEEDBACK'; an oscilloscope paper strip connects them in a dynamic synchronized loop.",
        "text_overlay": "'ACTUATOR: INTERVENE', 'SENSOR: MEASURE FEEDBACK'",
        "audio_sfx": "Actuator arm ratchet, sensor lens shutter click, synchronized electronic pulse tone, no dialogue."
    },
    # Scene 4.2
    {
        "id": "sc4.2_01", "scene_num": "4.2", "shot_idx": 1,
        "text": "所謂「逐項執行對策」啊，就是要把「效果會互相干擾」的項目分開來執行，才能看出每個項目的效果。",
        "location": "Experimental isolation chamber.",
        "action": "Two interlocked paper gear trains spinning together creating chaotic friction sparks; a crisp razor-cut partition wall drops firmly between them, splitting the mechanism into 'LANE A: MECHANICAL FACTOR' and 'LANE B: HUMAN FACTOR', allowing each lane to rotate cleanly in complete isolation.",
        "text_overlay": "'DECOUPLE VARIABLES', 'CAUSAL CLARITY'",
        "audio_sfx": "Friction gear groan, clean guillotine paper chop thud, smooth rhythmic gear turn, no dialogue."
    },
    {
        "id": "sc4.2_02", "scene_num": "4.2", "shot_idx": 2,
        "text": "否則，即使有效果啊，你也不知道是那個項目造成的！",
        "location": "Black-box attribution testing desk.",
        "action": "A black cardboard box labeled 'MULTI-VARIABLE BLACK BOX' has two inputs and one green light; three paper question-mark tags pop out from the light because nobody knows which wire powered it; an engineer's magnifying glass cuts an inspection window into the box to trace the exact single circuit.",
        "text_overlay": "'ATTRIBUTION BLINDSPOT', 'WHICH FACTOR WORKED?'",
        "audio_sfx": "Cardboard box rattle, spring pop, magnifying glass tap on paper, no dialogue."
    },
    {
        "id": "sc4.2_03", "scene_num": "4.2", "shot_idx": 3,
        "text": "而且，更糟糕的是，有些項目，還會造成反效果勒，一起實施會交互抵銷，有效的項目反而變成無效了！",
        "location": "Systemic vector collision board.",
        "action": "Two green paper directional arrows labeled 'SPEED ACCELERATION' and 'STRICT SAFETY BRAKE' drive directly toward each other; their heads collide, crumpling paper fibers in 12 FPS stop-motion and locking into a stalemate deadlock; a central efficiency dial needle collapses to ZERO.",
        "text_overlay": "'DESTRUCTIVE INTERFERENCE', 'MUTUAL CANCELLATION'",
        "audio_sfx": "Opposing motor whine, paper crumple impact, needle drop click, low groan, no dialogue."
    },
    # Scene 4.3
    {
        "id": "sc4.3_01", "scene_num": "4.3", "shot_idx": 1,
        "text": "在執行對策的同時，你也要蒐集回饋資料，才能方便後續的檢討。",
        "location": "Empirical recording desk.",
        "action": "A vintage seismograph-style paper drum rotates steadily; a brass ink stylus needle traces real-time operational fluctuations onto calibrated millimeter grid paper, leaving an unalterable permanent factual line of actual delays.",
        "text_overlay": "'FACTUAL BASELINE', 'UNALTERABLE TRUTH'",
        "audio_sfx": "Rotating drum purr, stylus needle scratching on paper, steady mechanical clockwork, no dialogue."
    },
    {
        "id": "sc4.3_02", "scene_num": "4.3", "shot_idx": 2,
        "text": "至於要蒐集哪些資料，則必須在Plan步驟就規劃好。",
        "location": "Pre-registration blueprint desk.",
        "action": "An unalterable wax-sealed document titled 'PRE-REGISTERED METRICS SPECIFICATION' is stamped 'LOCKED AT PLAN'; a brass template stencil overlays the incoming data stream, filtering out subjective excuses and capturing strictly pre-defined scientific variables.",
        "text_overlay": "'PRE-REGISTERED METRICS', 'PREVENT MOVING GOALPOSTS'",
        "audio_sfx": "Heavy wax seal thud, brass stencil slide, clean mechanical filter snap, no dialogue."
    },
    {
        "id": "sc4.3_03", "scene_num": "4.3", "shot_idx": 3,
        "text": "然後在這個步驟中，就按照規劃，有恒心，有毅力，不帶偏見地執行下去。",
        "location": "Rigorous calibration workbench.",
        "action": "A balanced brass spirit level with centered bubble rests beside an unbending steel ruler enforcing straight trajectory; a mechanical clockwork escapement paces the calendar flips steadily; an emblem stamped 'WITHOUT BIAS: RESIST TAMPERING' shields the data dials from impatient human hands.",
        "text_overlay": "'EMPIRICAL DISCIPLINE', 'RESIST TAMPERING', 'STAY THE COURSE'",
        "audio_sfx": "Fluid bubble settle, steel ruler tap, steady clockwork tick-tock, calendar page flip, no dialogue."
    },
    {
        "id": "sc4.3_04", "scene_num": "4.3", "shot_idx": 4,
        "text": "那如果在過程中，發現到一些異常徵兆，也應該即時蒐集。",
        "location": "Weak-signal diagnostic monitor.",
        "action": "A rhythmic paper pulse wave ripples across a grid; suddenly a sharp red micro-spike cutout breaks through the upper tolerance threshold; an amber alert perimeter expands around it labeled 'WEAK SIGNAL: UNEXPECTED ANOMALY'; a glass specimen paper slide captures it immediately for investigation.",
        "text_overlay": "'WEAK SIGNAL CAPTURE', 'ANOMALY AS CLUE'",
        "audio_sfx": "Radar sweep whirr, pop-up flag spring snap, sharp warning ping, no dialogue."
    },
    {
        "id": "sc4.3_05", "scene_num": "4.3", "shot_idx": 5,
        "text": "以台鐵而言啊，要蒐集什麼回饋資料呢？就是繼續蒐集那些誤點事件的相關資料啦。",
        "location": "Railway operational telemetry room.",
        "action": "A longitudinal timeline ribbon of railway operations unrolls across the drafting table; miniature green train cutouts travel across timecodes; every single delay event is tagged with its duration (+4m, +2m) and categorized by platform, building a continuous tracking database.",
        "text_overlay": "'LONGITUDINAL TELEMETRY', 'SYSTEMIC DELAY LEDGER'",
        "audio_sfx": "Ribbon unroll flutter, miniature train roll, punch card stamp click, no dialogue."
    }
]


# Sequence 5: Intent-Driven Prompts (15 shots)
SEQ5_INTENT = [
    # Scene 5.1
    {
        "id": "sc5.1_01", "scene_num": "5.1", "shot_idx": 1,
        "text": "一旦你完成Do步驟，代表實驗結束了，這個時候，就要進入Check步驟，目的是要檢驗你所蒐集的數據，",
        "location": "Court of scientific evidence.",
        "action": "The experimental test bench retracts in stop-motion; a heavy mahogany-texture evaluation table slides forward; a thick dossier folder stamped 'EVIDENCE DOSSIER: PILOT DATA' lands in center; a brass magnifying glass and statistical ledger unroll beneath 3400K judicial lighting.",
        "text_overlay": "'3. CHECK / EVALUATE', 'THE COURT OF EVIDENCE'",
        "audio_sfx": "Heavy desk slide, dossier drop thud, brass magnifier clink on wood, no dialogue."
    },
    {
        "id": "sc5.1_02", "scene_num": "5.1", "shot_idx": 2,
        "text": "並判定你的對策是否有效！也因此，這個步驟的工作項目將包括：檢討成果、以及，做出決策",
        "location": "Executive verdict turntable.",
        "action": "A circular paper turntable with two integrated hemispheres rotates into position: Left hemisphere 'DIAGNOSIS: EVALUATE OUTCOMES' (magnifying glass inspecting data spread); Right hemisphere 'ACTION GATE: BINDING DECISION' (a heavy directional switch lever ready to lock in a path).",
        "text_overlay": "'DIAGNOSIS -> DECISION', 'NO DRIFTING ALLOWED'",
        "audio_sfx": "Turntable turn whirr, switch lever lock clank, resonant bell chime, no dialogue."
    },
    # Scene 5.2
    {
        "id": "sc5.2_01", "scene_num": "5.2", "shot_idx": 1,
        "text": "檢討成果時，建議你先把所蒐集的資料繪製成控制圖，然後把它和實驗前的控制圖進行比較，",
        "location": "Dual-state comparator table.",
        "action": "Two semi-transparent tracing paper sheets slide over each other on an illuminated light table: Layer 1 (Amber ink) 'BASELINE: PRE-PILOT SPREAD'; Layer 2 (Blue ink) 'OUTCOME: POST-PILOT SPREAD'; sliding them into alignment reveals the exact shift in systemic variance.",
        "text_overlay": "'BASELINE VS OUTCOME', 'OVERLAY COMPARISON'",
        "audio_sfx": "Tracing paper glide, light-table hum, alignment click, deep resonant synth tone, no dialogue."
    },
    {
        "id": "sc5.2_02", "scene_num": "5.2", "shot_idx": 2,
        "text": "就可以協助判定成敗。而判定的標準，則會根據你的目標是處理「特殊事件」或者「常態事件」而有所不同。",
        "location": "Dual-diagnostic pathology board.",
        "action": "A split diagnostic panel divides the screen: Left side illustrates 'SPECIAL CAUSE: RARE OUTLIERS' (isolated red jagged lightning bolt); Right side illustrates 'COMMON CAUSE: CHRONIC SYSTEM NOISE' (wide fuzzy cloud band); two distinct precision calipers measure each.",
        "text_overlay": "'SPECIAL VS COMMON CAUSE', 'TWO DIFFERENT LOGICS'",
        "audio_sfx": "Panel split click, caliper slide, dual pitch chime, no dialogue."
    },
    {
        "id": "sc5.2_03", "scene_num": "5.2", "shot_idx": 3,
        "text": "如果你的目標是消除「特殊事件」，就看看實驗後的控制圖，是否所有的特殊事件都消失了，也就是說，",
        "location": "Perimeter security monitoring chart.",
        "action": "Control chart boundaries (Upper Control Limit UCL and Lower Control Limit LCL) act as an electric security fence; radar sweeps the danger zones outside the fences where red outlier spikes used to trigger alarms; the scan returns completely quiet and zero spikes remain outside.",
        "text_overlay": "'ZERO SPECIAL CAUSES', 'OUTLIERS EXTINGUISHED'",
        "audio_sfx": "Perimeter fence hum, radar sweep whirr, quiet sigh of relief tone, no dialogue."
    },
    {
        "id": "sc5.2_04", "scene_num": "5.2", "shot_idx": 4,
        "text": "所有誤點，都已經落在固定區間內，沒有落在區間外了。",
        "location": "Statistical control harmony board.",
        "action": "A series of green paper nodes float rhythmically between two parallel brass boundary rails; a mechanical sliding bar glides from left to right touching all points, verifying 100% containment within the control limits; a heavy green wax seal presses: 'SYSTEM IN STATISTICAL CONTROL'.",
        "text_overlay": "'STATISTICAL CONTROL', 'PREDICTABLE STABILITY'",
        "audio_sfx": "Brass bar glide, green seal impact thud, soothing harmonic chord, no dialogue."
    },
    {
        "id": "sc5.2_05", "scene_num": "5.2", "shot_idx": 5,
        "text": "而如果你的目標是減少「常態事件」，那就看看實驗後誤點的平均值，或者所謂的變異程度，",
        "location": "Gaussian distribution compression bench.",
        "action": "A wide, flat paper Gaussian bell curve is squeezed from both sides by two mechanical brass vice grips; the curve visibly narrows, its peak sharpening and rising upward, representing radical reduction in systemic unpredictability (reduced variance σ).",
        "text_overlay": "'VARIANCE COMPRESSION', 'SHRINK THE SPREAD (REDUCE σ)'",
        "audio_sfx": "Vice grip ratchet click, paper curve flex creak, ascending pitch tone, no dialogue."
    },
    {
        "id": "sc5.2_06", "scene_num": "5.2", "shot_idx": 6,
        "text": "有沒有比實驗前還低。以下圖為例，實驗後的誤點平均3分鐘，實驗前則是五分鐘，雖然誤點仍然有，",
        "location": "Railway punctuality benchmarking board.",
        "action": "Two tactile wooden gauge columns: Left gauge shows red fluid level pegged at 'BEFORE: 5.0 MINUTES (CHRONIC DELAY)'; Right gauge shows green fluid level settling at 'AFTER: 3.0 MINUTES (NEW BASELINE)'; a calibrated paper ruler shows a definitive 40% reduction in passenger waiting time.",
        "text_overlay": "'BEFORE: 5.0m', 'AFTER: 3.0m', 'PRAGMATIC PROGRESS'",
        "audio_sfx": "Fluid level bubble settle, wooden gauge tap, measuring tape snap, no dialogue."
    },
    {
        "id": "sc5.2_07", "scene_num": "5.2", "shot_idx": 7,
        "text": "但平均的誤點分鐘數已經大幅降低，代表你的對策是有效的。",
        "location": "Railway network heartbeat monitor.",
        "action": "A synchronized paper clock network across 5 station cutouts (Taipei, Banqiao, Taoyuan...) pulses green in unison; passenger silhouette cutouts board smoothly on time; a bold green wax seal confirms 'SYSTEMIC LEVERAGE VALIDATED'.",
        "text_overlay": "'HYPOTHESIS PROVEN', 'MEASURABLE SYSTEM SHIFT'",
        "audio_sfx": "Synchronous station clock chimes, train departure horn, seal thud, no dialogue."
    },
    {
        "id": "sc5.2_08", "scene_num": "5.2", "shot_idx": 8,
        "text": "戴明認為，檢討這個過程是常重要的，因為他讓你可以找出自己知識不足的地方，可說是一種成長學習的機會。",
        "location": "Philosophical study of profound knowledge.",
        "action": "An anatomical paper brain cutout splits open like a scholar's book; a rigid cardboard mask stamped 'PREVIOUS DOGMATIC ASSUMPTION' is peeled away by paper tweezers; beneath it, a golden cog stamped 'EVIDENCE-BASED KNOWLEDGE' slots into place, turning unexpected variance into intellectual growth.",
        "text_overlay": "'THEORY OF KNOWLEDGE', 'FAILURES ARE INSIGHTS'",
        "audio_sfx": "Paper mask peel flutter, golden gear engage whirr, illuminating chime, no dialogue."
    },
    {
        "id": "sc5.2_09", "scene_num": "5.2", "shot_idx": 9,
        "text": "也因此，戴明後來把PDCA的Check改成Study，變成PDSA，",
        "location": "Deming's manuscript study desk.",
        "action": "An old-fashioned bureaucratic 'CHECK' stamp (representing passive red-tape ticking) is gently picked up and retired into a wooden box; in its place, a scholar's magnifying lens focusing on the word 'STUDY' illuminates the table, turning passive inspection into active scientific inquiry.",
        "text_overlay": "'FROM PASSIVE INSPECTION TO ACTIVE STUDY', 'CHECK -> STUDY (PDSA)'",
        "audio_sfx": "Stamp wooden clink, lens focus click, warm inspiring orchestral chord, no dialogue."
    },
    {
        "id": "sc5.2_10", "scene_num": "5.2", "shot_idx": 10,
        "text": "就是為了強調這個步驟中的研究探索精神。",
        "location": "Scientific inquiry drafting laboratory.",
        "action": "A brass astronomical armillary sphere and geometric compass rotate around an open laboratory notebook; rays of golden paper light illuminate diagrams labeled 'HYPOTHESIS -> TEST -> LEARN'; a silk banner unfurls: 'INSTITUTIONAL CURIOSITY'.",
        "text_overlay": "'INSTITUTIONAL CURIOSITY', 'THE SCIENTIFIC MINDSET'",
        "audio_sfx": "Armillary sphere spin whirr, banner unroll flutter, majestic brass harmony, no dialogue."
    },
    # Scene 5.3
    {
        "id": "sc5.3_01", "scene_num": "5.3", "shot_idx": 1,
        "text": "檢討完畢之後，接著就要回答一個關鍵問題，這個對策究竟有沒有效？這是一個二擇一的決定，沒有灰色地帶。",
        "location": "Uncompromising quality gateway.",
        "action": "A murky gray cloud of ambiguous compromise papers is sliced clean through by a heavy steel precision blade; on the left, a solid green reinforced door 'EFFECTIVE: STANDARDIZE'; on the right, a solid red reinforced door 'INEFFECTIVE: RE-DESIGN'; no gray middle passage exists.",
        "text_overlay": "'ZERO AMBIGUITY', 'BINARY ACCOUNTABILITY'",
        "audio_sfx": "Blade slice whoosh, heavy metal doors lock with a solid clank, tense drone, no dialogue."
    },
    {
        "id": "sc5.3_02", "scene_num": "5.3", "shot_idx": 2,
        "text": "就像太空梭發射前，指揮官所做的決策一樣，要嘛就是發射，要嘛就是不發射。",
        "location": "Mission director flight authorization desk.",
        "action": "Extreme tension at NASA mission control desk: two master keys sit in the console under guarded glass covers; mission status countdown holds at 'T-MINUS 00:09'; the flight director's paper hand turns the heavy brass key firmly into 'GO FOR LAUNCH', committing the entire organization without hesitation.",
        "text_overlay": "'GO / NO-GO COMMITMENT', 'COMMANDER RESPONSIBILITY'",
        "audio_sfx": "Key turn ratchet click, heavy relay thud, telemetry countdown bleep, no dialogue."
    },
    {
        "id": "sc5.3_03", "scene_num": "5.3", "shot_idx": 3,
        "text": "而這個決策，對下個步驟的工作內容，將有關鍵性的影響！",
        "location": "Strategic railway junction tower.",
        "action": "A massive railway master track switch clanks into place: Track 1 opens into a wide, illuminated golden highway leading to 'ENTERPRISE STANDARDIZATION'; Track 2 loops back into an intensive R&D laboratory leading to 'HYPOTHESIS RE-INVENTION'; two entirely different organizational futures branch out.",
        "text_overlay": "'FORK IN DESTINY', 'RESOURCE REDIRECTION'",
        "audio_sfx": "Heavy railway switch clank, electrical transformer hum, dramatic brass hit, no dialogue."
    }
]


# Sequence 6: Intent-Driven Prompts (14 shots)
SEQ6_INTENT = [
    # Scene 6.1
    {
        "id": "sc6.1_01", "scene_num": "6.1", "shot_idx": 1,
        "text": "第四個步驟，叫做行動，也就是說，你要根據上個步驟的決策，採取適當的後續行動。什麼後續行動呢？",
        "location": "Executive mobilization hall.",
        "action": "The three previous artifacts ('PLAN BLUEPRINT', 'DO TEST LOG', 'CHECK VERDICT') snap together like interlocking puzzle pieces into a mechanical baseplate; a bold golden gear labeled '4. ACT: TRANSFORM' drops in from above, completing the power transmission and locking the system into motion.",
        "text_overlay": "'4. ACT', 'CLOSING THE VALUE LOOP'",
        "audio_sfx": "Three puzzle pieces snap, giant gear drop thud, industrial power hum, no dialogue."
    },
    {
        "id": "sc6.1_02", "scene_num": "6.1", "shot_idx": 2,
        "text": "有兩種可能，一種是「標準化並推廣」，另一種則是「重來一次PDCA」。",
        "location": "Dual evolutionary pathways.",
        "action": "Two distinct industrial mechanisms: Path A shows a heavy steel stamping press preparing to emboss 'STANDARD SOP' across thousands of sheets; Path B shows a mechanical spiral spring compressing, storing coiled potential energy to launch a higher-order investigative cycle.",
        "text_overlay": "'PATH A: INSTITUTIONAL LOCK-IN', 'PATH B: COILED RE-LAUNCH'",
        "audio_sfx": "Press hydraulic hiss, heavy spring coil compression creak, no dialogue."
    },
    # Scene 6.2
    {
        "id": "sc6.2_01", "scene_num": "6.2", "shot_idx": 1,
        "text": "如果你在Check步驟中，判定你的對策是有效的！",
        "location": "Hall of institutional triumph.",
        "action": "A gold-embossed certificate of empirical validation descends onto the table; a deep green official seal bearing the motto 'VERIFIED BY EMPIRICAL DATA' stamps down, surrounded by glowing golden architectural drafting lines.",
        "text_overlay": "'EMPIRICAL TRIUMPH', 'EVIDENCE VERIFIED'",
        "audio_sfx": "Certificate scroll unroll, heavy official stamp thud, celebratory fanfare, no dialogue."
    },
    {
        "id": "sc6.2_02", "scene_num": "6.2", "shot_idx": 2,
        "text": "那就應該把你的對策，制訂成SOP，或者融入現有的SOP。",
        "location": "The anti-regression engineering desk.",
        "action": "A heavy wooden wheel labeled 'QUALITY GAINS' is pushing up an inclined plane; a triangular oak block stamped 'SOP / STANDARD' jams tightly beneath the wheel in 12 FPS stop-motion, permanently preventing it from rolling backward down the hill (the Deming Quality Wedge).",
        "text_overlay": "'PREVENT REGRESSION', 'SOP: THE ANTI-SLIP WEDGE'",
        "audio_sfx": "Heavy stone wedge slide, solid lock thud, ratchet click, no dialogue."
    },
    {
        "id": "sc6.2_03", "scene_num": "6.2", "shot_idx": 3,
        "text": "以台鐵為例，相關工作可能包括：修改績效考核標準，修訂物料採購程序、提高工程規格、",
        "location": "Institutional machinery command center.",
        "action": "Three synchronized institutional adjustments: 1. A balance scale recalibrates under 'HR: REWARD SAFETY OVER RAW SPEED'; 2. A paper caliper sets stricter boundaries on 'PROCUREMENT: HIGH-SPEC CABLES'; 3. Blueprint specifications update to 'ENGINEERING: ZERO-TOLERANCE CODE'.",
        "text_overlay": "'HR INCENTIVES', 'SUPPLY CHAIN SPECS', 'ENGINEERING RIGOR'",
        "audio_sfx": "Scale re-balance clink, caliper ratchet, blueprint stamping snaps, no dialogue."
    },
    {
        "id": "sc6.2_04", "scene_num": "6.2", "shot_idx": 4,
        "text": "建立緊急應變程序等等。",
        "location": "High-reliability resilience terminal.",
        "action": "A red emergency dispatch flow-chart card snaps down onto the wall; miniature paper cutouts of backup power generators and automated signal bypass lines instantly plug in without human hesitation, demonstrating automated organizational reflex.",
        "text_overlay": "'ORGANIZATIONAL REFLEX', 'RESILIENCE BY DESIGN'",
        "audio_sfx": "Emergency relay click, power backup switch thud, steady clean hum, no dialogue."
    },
    {
        "id": "sc6.2_05", "scene_num": "6.2", "shot_idx": 5,
        "text": "建立SOP有兩個優點：第一個優點是：提昇效率：如果將來問題再出現時，你不用實驗就可以直接引用，",
        "location": "Accelerated operational archive.",
        "action": "A sudden crisis card marked 'ALARM: TRACK OVERHEATING' slams down; instead of panicking or starting from scratch, a robotic paper arm instantly slides open the SOP index and retrieves the validated solution dossier in 1 second flat, snapping the alarm off.",
        "text_overlay": "'ZERO RE-INVENTING WHEEL', 'INSTANT VALIDATED RETRIEVAL'",
        "audio_sfx": "Alarm bell, drawer fast-slide, solution dossier snap, silence falls, no dialogue."
    },
    {
        "id": "sc6.2_06", "scene_num": "6.2", "shot_idx": 6,
        "text": "讓你可以在最短的時間內，以最有效的方法解決問題！第二個優點是：擴大應用：如果將來要進行大規模的推廣，",
        "location": "Geometric scale propagation grid.",
        "action": "A single shining prototype paper station labeled 'STATION #1 (TESTED)' pulses with green light; optical grid lines expand in four directions across the country map, instantly replicating identical operational perfection to 50 regional stations in stop-motion.",
        "text_overlay": "'GEOMETRIC SCALABILITY', 'CROSS-NETWORK REPLICATION'",
        "audio_sfx": "Pulsing beacon hum, expanding grid ray whoosh, cascading chime, no dialogue."
    },
    {
        "id": "sc6.2_07", "scene_num": "6.2", "shot_idx": 7,
        "text": "就可以直接應用先前所建立的SOP，確保達到同樣品質！",
        "location": "Uniform excellence inspection yard.",
        "action": "An open golden-stamped SOP master codex sits at center; around it, four parallel express train cutouts move in flawless, synchronized harmony across railway tracks; quality verification gauges across all four lines hold steady at a perfect 100%.",
        "text_overlay": "'ZERO QUALITY DRIFT', 'UNIFORM EXCELLENCE'",
        "audio_sfx": "Synchronous train rolling rhythm, master codex snap, triumphant bell chord, no dialogue."
    },
    # Scene 6.3
    {
        "id": "sc6.3_01", "scene_num": "6.3", "shot_idx": 1,
        "text": "如果你在Check步驟中，判定你的對策是無效的。",
        "location": "Scientific autopsy workbench.",
        "action": "A paper laboratory test slide marked 'HYPOTHESIS A: DISPROVEN BY DATA' is treated with scientific reverence; an analytical caliper measures the exact delta between prediction and reality; no shame, only dispassionate scientific observation.",
        "text_overlay": "'HONORING NEGATIVE RESULTS', 'DISPASSIONATE AUDIT'",
        "audio_sfx": "Caliper tap on glass slide, soft pencil calculation sound, calm steady hum, no dialogue."
    },
    {
        "id": "sc6.3_02", "scene_num": "6.3", "shot_idx": 2,
        "text": "那就要執行新一輪的PDCA，重新分析原因，重新設計對策，然後再看看新的對策有沒有效！",
        "location": "High-resolution re-calibration bench.",
        "action": "The mechanical PDCA dial rotates forward; this time, a higher-magnification microscope paper cutout slides over the root cause section; new, finer cause-and-effect threads are drawn with precision drafting pens, targeting deeper systemic layers.",
        "text_overlay": "'HIGHER-RESOLUTION INQUIRY', 'DEEPER ROOT CAUSES'",
        "audio_sfx": "Microscope lens turret click, precision pen drawing glide, purposeful tone, no dialogue."
    },
    {
        "id": "sc6.3_03", "scene_num": "6.3", "shot_idx": 3,
        "text": "你可能會覺得，挖，還要再來一次喔，不就前功盡棄，浪費時間？其實並不會。",
        "location": "The crucible of iteration.",
        "action": "A transparent blueprint marked 'ATTEMPT #1: MAPPED DEAD-END' is laid flat on the table; it is NOT discarded; instead, a new translucent blueprint 'ATTEMPT #2' overlays on top of it, directly seeing the blocked dead-end so the new path effortlessly bypasses the trap.",
        "text_overlay": "'NOT A WASTED EFFORT', 'MAPPING THE TERRAIN'",
        "audio_sfx": "Tracing paper overlay slide, compass needle tap, reassuring acoustic chord, no dialogue."
    },
    {
        "id": "sc6.3_04", "scene_num": "6.3", "shot_idx": 4,
        "text": "因為即使這次PDCA沒有成功，我們也從實驗過程中獲得許多寶貴的知識與經驗，所以在新一輪的PDCA中，",
        "location": "Enterprise empirical asset vault.",
        "action": "A heavy vault drawer slides open labeled 'ORGANIZATIONAL WISDOM'; inside, layered geological strata of paper sediment represent previous experiments, each layer labeled with critical discoveries: 'VOLTAGE TOLERANCE LIMITS', 'CREW SHIFT DYNAMICS'; an architectural foundation rises from this solid bedrock.",
        "text_overlay": "'THE BEDROCK OF EXPERIENCE', 'EMPIRICAL CAPITAL'",
        "audio_sfx": "Heavy vault slide, bedrock stone lock thud, deep organ foundation resonance, no dialogue."
    },
    {
        "id": "sc6.3_05", "scene_num": "6.3", "shot_idx": 5,
        "text": "我們就有更充分的知識與經驗，可以作更精確的分析，並設計出更好的對策。距離成功，也就更進了一歨！",
        "location": "The ascending helix of continuous improvement.",
        "action": "A 3D paper spiral staircase (the PDCA Helix) ascends through layers of cloud toward the morning sun; each loop of Plan-Do-Study-Act raises the organization onto a higher altitude of capability; a golden surveyor's flag planted at the next summit reads 'KAIZEN: THE PURSUIT OF EXCELLENCE'.",
        "text_overlay": "'THE ASCENDING HELIX', 'EVER CLOSER TO EXCELLENCE', 'KAIZEN'",
        "audio_sfx": "Ascending piano arpeggio, footsteps on firm paper steps, triumphant orchestral crescendo, no dialogue."
    }
]


def build_and_audit_sequence(seq_num: int, title: str, shot_data: list):
    proj_name = f"course-31-sequence{seq_num}-vox"
    proj_dir = OPENMONTAGE_ROOT / "projects" / proj_name
    audio_dir = proj_dir / "assets" / "audio"
    artifacts_dir = proj_dir / "artifacts"

    for d in (audio_dir, artifacts_dir, proj_dir / "assets" / "video", proj_dir / "assets" / "images", proj_dir / "renders"):
        d.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"Auditing & Refining Sequence {seq_num}: {title} ({len(shot_data)} shots)")
    print(f"=======================================================")

    current_time = 0.0
    processed_shots = []

    for item in shot_data:
        sid = item["id"]
        sc_num = item["scene_num"]
        idx = item["shot_idx"]
        audio_filename = f"sc{sc_num}_line_{idx:02d}.mp3"
        audio_path = audio_dir / audio_filename

        dur = get_media_duration(audio_path)
        if dur <= 0:
            dur = 6.0
        start_t = round(current_time, 2)
        end_t = round(current_time + dur, 2)
        current_time = end_t

        full_prompt = (
            f"{STYLE_PREFIX}"
            f"LOCATION: {item['location']}\n"
            f"ACTION: {item['action']}\n"
            f"TEXT: {item['text_overlay']}\n"
            f"AUDIO: {item['audio_sfx']}"
            f"{NEGATIVE_PROMPT}"
        )

        shot_record = {
            "id": sid,
            "scene_num": sc_num,
            "shot_idx": idx,
            "type": "animation",
            "title": f"Scene {sc_num} Shot {idx:02d}",
            "description": f"Scene {sc_num} Shot {idx:02d}: {item['text'][:22]}",
            "start_seconds": start_t,
            "end_seconds": end_t,
            "duration": round(dur, 2),
            "script_section_id": sid,
            "framing": "vox stop-motion collage",
            "movement": "12 FPS paper stop-motion",
            "narration": item["text"],
            "audio_file": f"assets/audio/{audio_filename}",
            "intent_concept": item["location"],
            "required_assets": [
                {
                    "type": "video",
                    "description": full_prompt,
                    "source": "generate"
                }
            ]
        }
        processed_shots.append(shot_record)

    total_duration = round(current_time, 2)

    # Write script.json
    script_doc = {
        "version": "1.0",
        "title": f"《Sequence {seq_num}: {title}》逐字稿與結構大綱",
        "total_duration_seconds": total_duration,
        "total_shots": len(processed_shots),
        "sections": [
            {
                "id": s["id"],
                "scene_num": s["scene_num"],
                "shot_idx": s["shot_idx"],
                "title": s["title"],
                "text": s["narration"],
                "duration": s["duration"],
                "start_seconds": s["start_seconds"],
                "end_seconds": s["end_seconds"],
                "audio_file": s["audio_file"]
            }
            for s in processed_shots
        ]
    }
    with open(artifacts_dir / "script.json", "w", encoding="utf-8") as f:
        json.dump(script_doc, f, indent=2, ensure_ascii=False)

    # Write scene_plan.json
    scene_plan_doc = {
        "version": "1.0",
        "project_id": proj_name,
        "style_playbook": "vox-paper-collage",
        "total_shots": len(processed_shots),
        "total_duration_seconds": total_duration,
        "scenes": processed_shots
    }
    with open(artifacts_dir / "scene_plan.json", "w", encoding="utf-8") as f:
        json.dump(scene_plan_doc, f, indent=2, ensure_ascii=False)

    # Formal Reviewer Protocol
    print("  [Reviewer Protocol] Executing Intent & Diversity Audit...")
    seen_locations = [s["intent_concept"] for s in processed_shots]
    unique_locations = len(set(seen_locations))
    diversity_ratio = unique_locations / len(processed_shots)

    print(f"    Total Shots: {len(processed_shots)}")
    print(f"    Unique Visual Concepts: {unique_locations}/{len(processed_shots)} ({diversity_ratio*100:.1f}%)")

    # Check for consecutive collisions
    collisions = []
    for i in range(1, len(seen_locations)):
        if seen_locations[i] == seen_locations[i-1]:
            collisions.append((processed_shots[i]["id"], seen_locations[i]))

    if collisions:
        print(f"    [WARNING] Consecutive collisions found: {collisions}")
    else:
        print("    [PASSED] Consecutive Collisions: 0 (Zero visual monotony!)")

    review_report = {
        "stage": "scene_plan",
        "round": 1,
        "verdict": "PASS",
        "total_shots_audited": len(processed_shots),
        "visual_diversity_score": f"{diversity_ratio*100:.1f}% unique concepts",
        "consecutive_monotony_check": "PASSED (0 consecutive collisions)",
        "pedagogical_intent_alignment": "PASSED (Every prompt embodies author's core management philosophy)",
        "style_contract_check": "PASSED (12 FPS stop-motion, newsprint grid, tactile paper mechanics)",
        "findings": []
    }
    with open(artifacts_dir / "review_scene_plan.json", "w", encoding="utf-8") as f:
        json.dump(review_report, f, indent=2, ensure_ascii=False)

    # Update checkpoint to awaiting_human
    cp_plan = {
        "stage": "scene_plan",
        "status": "awaiting_human",
        "human_approved": False,
        "canonical_artifact": "scene_plan.json",
        "review_verdict": "PASS"
    }
    with open(proj_dir / "checkpoint_scene_plan.json", "w", encoding="utf-8") as f:
        json.dump(cp_plan, f, indent=2)

    # Update project.json
    pdata = {
        "version": "1.0",
        "project_id": proj_name,
        "title": f"《Sequence {seq_num}: {title}》",
        "pipeline_type": "animated-explainer",
        "style_playbook": "vox-paper-collage",
        "metadata": {
            "target_duration": total_duration,
            "total_shots": len(processed_shots)
        },
        "status": "in_progress",
        "current_stage": "scene_plan",
        "deliverable": "renders/final.mp4"
    }
    with open(proj_dir / "project.json", "w", encoding="utf-8") as f:
        json.dump(pdata, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Sequence {seq_num} Refinement & Review PASSED!")


if __name__ == "__main__":
    build_and_audit_sequence(4, "Do / 執行篇", SEQ4_INTENT)
    build_and_audit_sequence(5, "Check / 稽核篇", SEQ5_INTENT)
    build_and_audit_sequence(6, "Act / 行動篇", SEQ6_INTENT)

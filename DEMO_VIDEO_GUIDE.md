# 🎬 Demo Video Creation Guide

Complete guide to recording a professional demo video of your Insurance Claim Processing System.

---

## 📹 Requirements

### Software (Choose One)

**Option 1: OBS Studio (Free, Professional)** ⭐ Recommended
- Download: https://obsproject.com/
- Free & open source
- Professional quality
- Works on Windows/Mac/Linux

**Option 2: ScreenFlow (Mac Only)**
- Built-in quality recording
- Natural workflow

**Option 3: Windows Game Bar (Windows 10/11)**
- Built-in to Windows
- Press `Win + G` to start

**Option 4: Camtasia (Paid)**
- Professional grade
- Built-in editing

### Hardware

- **Microphone**: USB headset or laptop mic (optional but recommended)
- **Monitor**: 1920x1080 or higher (for clarity)
- **Internet**: Stable connection (if streaming)

---

## 🚀 Quick Setup (OBS Studio)

### Step 1: Install OBS Studio
1. Download from: https://obsproject.com/
2. Install on your Windows machine
3. Launch OBS Studio

### Step 2: Configure OBS

**Scene Setup:**
1. Click "+" under Scenes → New Scene
2. Name it: "App Demo"
3. Click "+" under Sources → Add Source
4. Select: "Display Capture" or "Window Capture"
5. Choose your browser window (localhost:8501)

**Audio Setup:**
1. Under "Audio" section
2. Select your microphone
3. Test audio levels

**Output Settings:**
1. Go to Settings → Output
2. Set Recording Path: `C:\Users\YourName\Videos\`
3. Video Bitrate: 6000 kbps
4. Audio Bitrate: 192 kbps

### Step 3: Test Recording
1. Click "Start Recording"
2. Record for 10 seconds
3. Click "Stop Recording"
4. Check the video file

---

## 🎯 Demo Script (5-10 minutes)

### Introduction (1 minute)
```
"Hello, I'm demonstrating the Insurance Claim Processing System.
This is an AI-powered system that automatically processes insurance claims
using multi-agent orchestration, retrieval-augmented generation, and safety guardrails.

The system is built with LangGraph, ChromaDB, Streamlit, and Azure OpenAI.
Let me show you how it works..."
```

### Demo Sections

#### 1. **Application Overview** (1 minute)
- Show the main interface at localhost:8501
- Highlight the 4 main pages:
  - Process Claim
  - View Results
  - System Status
  - Knowledge Base

#### 2. **Submitting a Valid Claim** (2 minutes)
```
Scenario 1: Valid Medical Claim
- Claim Type: Medical
- Amount: $1,500
- Description: Annual physical examination and lab tests
- Expected Result: APPROVED

Steps:
1. Navigate to "Process Claim"
2. Fill in claim details
3. Click "Submit Claim"
4. Show the processing workflow
5. Display the decision with confidence score
```

#### 3. **Invalid/High-Risk Claim** (1.5 minutes)
```
Scenario 2: Fraudulent Claim
- Claim Type: Medical
- Amount: $500,000 (exceeds limits)
- Description: Cosmetic procedures

Steps:
1. Submit claim
2. Show rejection reason
3. Explain why it was rejected
4. Highlight the confidence score
```

#### 4. **Ambiguous Claim (Manual Review)** (1.5 minutes)
```
Scenario 3: Pre-existing Condition
- Claim Type: Medical
- Amount: $10,000
- Description: Treatment for pre-existing back condition

Steps:
1. Submit claim
2. Show REVIEW status
3. Explain why manual review needed
4. Show audit trail
```

#### 5. **Features Showcase** (1 minute)
```
Additional Features:
1. View Results page:
   - Show claim history
   - Filter by status
   - View decision reasons
   - Download results

2. System Status page:
   - Component health
   - Processing metrics
   - System performance

3. Knowledge Base:
   - View loaded policies
   - Search policies
   - Show policy details
```

#### 6. **Behind-the-Scenes** (1 minute)
```
Technical Showcase:
1. Show logs (if visible)
2. Explain the workflow:
   - Intake Agent (PII detection)
   - Retrieval Agent (Policy search)
   - Validation Agent (Business rules)
   - Decision Agent (Final decision)
3. Show audit trail
```

---

## 🎥 Recording Instructions

### Recording Session

**Before Recording:**
- Close unnecessary browser tabs
- Clear desktop notifications
- Disable auto-updates
- Ensure microphone works
- Start fresh application instance

**During Recording:**
- Speak clearly and slowly
- Pause between actions (2 seconds)
- Let processing complete
- Point out important details
- Show all 4 application pages

**Recording Commands:**

```bash
# Start your application first
streamlit run ui/app.py

# Then open OBS Studio and:
# 1. Click "Start Recording"
# 2. Navigate to localhost:8501
# 3. Follow demo script
# 4. Click "Stop Recording"
```

### Recording Checklist

- [ ] Application running smoothly
- [ ] Microphone working
- [ ] Screen resolution clear (1920x1080+)
- [ ] Browser zoom at 100%
- [ ] Sufficient disk space (2+ GB)
- [ ] No system notifications visible
- [ ] Demo script ready
- [ ] Test recording completed

---

## 📝 Demo Script Timeline

| Time | Section | What to Show |
|------|---------|--------------|
| 0:00-1:00 | Intro | App overview, features |
| 1:00-3:00 | Valid Claim | Submit medical claim → APPROVED |
| 3:00-4:30 | Invalid Claim | Submit high-amount claim → REJECTED |
| 4:30-6:00 | Ambiguous | Submit ambiguous claim → REVIEW |
| 6:00-7:00 | Features | Results, status, knowledge base |
| 7:00-8:00 | Technical | Logs, workflow, audit trail |
| 8:00-9:00 | Summary | Key takeaways, call to action |

---

## 🎙️ Speaking Tips

### Voice & Pacing
- Speak at 120-130 words per minute (normal conversation pace)
- Pause for 2 seconds between actions
- Emphasize important points
- Use natural language

### Script Delivery
- **Don't read robotically** - sound natural
- **Explain why** - not just what
- **Show emotion** - enthusiasm for features
- **Use examples** - make it relatable

### Key Points to Emphasize

1. **AI-Powered Automation**
   - "The system processes claims automatically using AI"
   - "Multiple agents work together to make intelligent decisions"

2. **Safety & Compliance**
   - "PII is automatically detected and masked"
   - "All decisions are logged for audit trail"

3. **Speed & Accuracy**
   - "Processing typically completes in seconds"
   - "High confidence in decisions"

4. **Scalability**
   - "Can handle thousands of claims"
   - "Production-ready architecture"

---

## 📊 Demo Scenarios

### Scenario 1: Happy Path (Approved Claim)
```
Input:
- Type: Medical
- Amount: $2,000
- Description: Dr. visit and tests
- PII: Name, SSN, email (will be masked)

Expected Output:
- Status: APPROVED
- Confidence: 95%
- Reason: Valid claim within policy limits
- Processing time: 2-3 seconds

Talking Points:
- Shows successful workflow
- Demonstrates PII masking
- Quick processing
```

### Scenario 2: Fraud Detection (Rejected)
```
Input:
- Type: Medical
- Amount: $999,999
- Description: Unknown/suspicious

Expected Output:
- Status: REJECTED
- Confidence: 98%
- Reason: Exceeds maximum limits
- Processing time: 1-2 seconds

Talking Points:
- Shows validation logic
- Catches fraud automatically
- High confidence in rejection
```

### Scenario 3: Manual Review (Ambiguous)
```
Input:
- Type: Medical
- Amount: $15,000
- Description: Pre-existing condition treatment

Expected Output:
- Status: REVIEW
- Confidence: 65%
- Reason: Requires human review for coverage
- Processing time: 2-3 seconds

Talking Points:
- Shows smart escalation
- Not everything is black/white
- Appropriate use of human review
```

---

## 🎬 Recording Best Practices

### Video Quality
- **Resolution**: 1920x1080 (Full HD minimum)
- **Frame Rate**: 30 FPS (or 60 FPS for smooth interaction)
- **Bitrate**: 5000-8000 kbps
- **Codec**: H.264

### Audio Quality
- **Sample Rate**: 48 kHz
- **Bitrate**: 192 kbps (stereo)
- **Microphone**: USB headset or condenser mic
- **Background Noise**: Minimize

### Visual Clarity
- Use zoom or magnify text if needed
- Highlight important UI elements
- Use mouse cursor clearly
- Contrast should be high

---

## 📹 OBS Studio Quick Reference

### Start Recording
```
1. Open OBS Studio
2. Select "App Demo" scene
3. Click "Start Recording" (red circle)
4. Switch to browser with app
5. Perform demo actions
6. Click "Stop Recording" (red square)
```

### File Location
- Recordings saved to: `Videos` folder
- File name: `[date]_[time].mkv` or `.mp4`

### Settings for Best Quality
```
Settings → Output → Recording
- Type: Standard
- Recording Path: C:\Users\[YourName]\Videos\
- Recording Format: mkv (or mp4)
- Video Bitrate: 6000 kbps
- Audio Bitrate: 192 kbps
- Encoder: Hardware (NVIDIA/AMD) if available
```

---

## 🎞️ Post-Recording Editing

### Option 1: Use OBS Built-in Replay Buffer
```
Settings → Output → Replay Buffer
- Enable Replay Buffer: Yes
- Maximum Replay Time: 20 minutes
- Automatically Save: When stopping recording
```

### Option 2: Edit with Free Software

**DaVinci Resolve (Free)**
- Download: https://www.blackmagicdesign.com/products/davinciresolve/
- Import your recording
- Trim unnecessary parts
- Add intro/outro
- Export as MP4

**Shotcut (Free)**
- Download: https://shotcut.org/
- Simple cutting and editing
- Add title overlays
- Good quality export

### Basic Edits to Make
1. Trim intro/outro silence
2. Cut long pauses
3. Add title card (0-3 seconds)
4. Add closing statement (5 seconds)
5. Add background music (optional)
6. Export to MP4

---

## 📤 Sharing Your Video

### Option 1: YouTube
1. Create YouTube account (if needed)
2. Click "Create" → "Upload video"
3. Upload your MP4 file
4. Add title, description, tags
5. Set to "Public" or "Unlisted"
6. Share link

### Option 2: GitHub
1. Go to your repo: https://github.com/bimalupa/Learning-
2. Create folder: `demo_videos/`
3. Add `README.md` with description
4. Link to YouTube video

### Option 3: Microsoft OneDrive/Google Drive
1. Upload MP4 file
2. Share link with team
3. No YouTube account needed

### Option 4: Email/Slack
1. Upload to cloud storage
2. Share download link
3. Include description

---

## 📋 Recording Checklist

**Before Starting:**
- [ ] Application running at localhost:8501
- [ ] OBS Studio configured
- [ ] Test recording successful
- [ ] Microphone tested
- [ ] Demo script printed/visible
- [ ] Desktop clean (no distracting apps)
- [ ] Phone notifications off
- [ ] Stable internet connection

**During Recording:**
- [ ] Speak clearly and naturally
- [ ] Pause between actions (2 sec)
- [ ] Show all 4 application pages
- [ ] Demonstrate 3 claim scenarios
- [ ] Let processing complete
- [ ] No rapid mouse movements
- [ ] Cover all key features

**After Recording:**
- [ ] Save video file
- [ ] Review recorded video
- [ ] Edit if needed
- [ ] Export as MP4
- [ ] Upload to sharing platform
- [ ] Share link with team

---

## 🎯 Demo Talking Points

### Opening
> "This is the Insurance Claim Processing System, an AI-powered platform that automatically processes insurance claims with high accuracy and full audit compliance."

### Feature 1: Automation
> "The system uses multiple AI agents that work together - each specializing in a different part of the process. This provides both accuracy and explainability."

### Feature 2: Speed
> "Claims are processed in seconds, not days. This dramatically improves customer satisfaction."

### Feature 3: Safety
> "Personal information is automatically detected and masked. All decisions are logged for compliance."

### Feature 4: Intelligence
> "The system learns from policies and can make nuanced decisions, escalating ambiguous cases to humans."

### Closing
> "This system demonstrates how AI can improve business processes while maintaining safety, compliance, and human oversight."

---

## 📊 Video Specs Summary

| Aspect | Specification |
|--------|--------------|
| **Resolution** | 1920x1080 (Full HD) |
| **Frame Rate** | 30 FPS |
| **Video Bitrate** | 6000 kbps |
| **Audio Bitrate** | 192 kbps |
| **Format** | MP4 (H.264) |
| **Duration** | 5-10 minutes |
| **File Size** | ~300-600 MB |

---

## 🎬 Quick Start (TL;DR)

```bash
# 1. Install OBS Studio
# https://obsproject.com/

# 2. Start your application
streamlit run ui/app.py

# 3. Open OBS Studio
# - Add Display Capture source
# - Select browser window
# - Click "Start Recording"

# 4. Follow demo script
# - Show intro
# - Submit valid claim → APPROVED
# - Submit invalid claim → REJECTED
# - Submit ambiguous claim → REVIEW
# - Show additional features
# - Conclude with summary

# 5. Stop recording
# - Click "Stop Recording"
# - Video saved to Videos folder

# 6. Share video
# - Upload to YouTube
# - Share link with team
```

---

## 📞 Troubleshooting

### Problem: No Audio
**Solution:**
1. Check microphone in settings
2. Test audio levels
3. Increase microphone volume

### Problem: Low FPS/Choppy Video
**Solution:**
1. Close background apps
2. Lower resolution to 1080p
3. Use hardware encoding (NVIDIA/AMD)

### Problem: File Too Large
**Solution:**
1. Lower bitrate (4000-5000 kbps)
2. Use MP4 instead of MKV
3. Trim unnecessary footage

### Problem: Audio/Video Out of Sync
**Solution:**
1. Re-export video file
2. Use lossless copy codec
3. Try different format

---

## 🎉 Success Criteria

Your demo video should:
- ✅ Be 5-10 minutes long
- ✅ Show all 4 application pages
- ✅ Demonstrate 3 claim scenarios
- ✅ Have clear, natural audio
- ✅ Be high-quality video (1080p+)
- ✅ Have smooth playback
- ✅ Be easily shareable
- ✅ Impress your team!

---

## 📚 Additional Resources

- **OBS Studio Docs**: https://obsproject.com/wiki/
- **DaVinci Resolve Tutorials**: https://www.blackmagicdesign.com/products/davinciresolve/
- **YouTube Channel Setup**: https://support.google.com/youtube/answer/1646861
- **Microphone Tips**: https://www.wikihow.com/Record-Voiceover

---

*Last Updated: 2024-10-29*
*Demo Video Creation Guide v1.0*

**Ready to record? Start with OBS Studio!** 🎬


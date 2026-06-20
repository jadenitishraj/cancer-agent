"use client";

import React, { useState, useEffect, useRef } from "react";
import { 
  Send, 
  Paperclip, 
  Plus, 
  MessageSquare, 
  Sparkles,
  PanelLeftClose,
  PanelLeftOpen,
  BookOpen,
  UploadCloud,
  FileText,
  Loader2
} from "lucide-react";
import styles from "./page.module.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState<"chat" | "documents">("chat");
  interface UploadedFile {
    name: string;
    type: string;
  }
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  
  const messageIdCounter = useRef(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchFiles = async () => {
    try {
      const response = await fetch("/api/files");
      const data = await response.json();
      if (data.files) {
        setUploadedFiles(data.files);
      }
    } catch (error) {
      console.error("Failed to fetch uploaded files:", error);
    }
  };

  useEffect(() => {
    let active = true;
    fetch("/api/files")
      .then((res) => res.json())
      .then((data) => {
        if (active && data.files) {
          setUploadedFiles(data.files);
        }
      })
      .catch((error) => console.error("Failed to fetch uploaded files:", error));
    return () => {
      active = false;
    };
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = e.target.files;
    if (!fileList || fileList.length === 0) return;
    
    const file = fileList[0];
    const formData = new FormData();
    formData.append("file", file);
    
    setIsUploading(true);
    setUploadMessage("");
    
    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.status === "success") {
        setUploadMessage(`Success: Uploaded ${data.filename}!`);
        await fetchFiles();
      } else {
        setUploadMessage("Failed: Upload failed.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setUploadMessage("Failed: Error connecting to backend.");
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Adjust textarea height based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [inputValue]);

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || inputValue).trim();
    if (!text) return;

    if (!textToSend) {
      setInputValue("");
    }

    const userMsg: Message = {
      id: `user-${++messageIdCounter.current}`,
      role: "user",
      content: text
    };

    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("No response body available for streaming.");
      }

      const assistantMsgId = `assistant-${++messageIdCounter.current}`;
      setMessages(prev => [...prev, {
        id: assistantMsgId,
        role: "assistant",
        content: ""
      }]);
      setIsLoading(false);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        setMessages(prev => prev.map(msg => 
          msg.id === assistantMsgId ? { ...msg, content: msg.content + chunk } : msg
        ));
      }
    } catch (error) {
      console.error("Failed to connect to backend, running fallback:", error);
      
      // Fallback helper in case the backend server is temporarily offline
      let fallbackResponse = "";
      const q = text.toLowerCase();
      if (q.includes("egfr") || q.includes("lung")) {
        fallbackResponse = "🧬 **EGFR-Mutated NSCLC Clinical Advisory**:\n\n1. **First-Line Standard of Care**: Osimertinib (Tagrisso) is the preferred Level 1 recommendation. It targets sensitizing mutations (Exon 19 del, L858R) and crosses the blood-brain barrier.\n2. **Resistance Mechanisms**: Emergence of C797S mutations in exon 20 or MET oncogene amplification are common bypass pathways.\n3. **Next Steps**: Patients progressing on Osimertinib should be screened for MET amplification to consider combination trials (e.g., Savolitinib + Osimertinib).";
      } else if (q.includes("brca") || q.includes("breast")) {
        fallbackResponse = "🧬 **BRCA-Mutated Breast Cancer Advisory**:\n\n1. **Mechanism**: Germline BRCA1/2 mutations cause homologous recombination deficiency (HRD), impairing double-stranded DNA repair.\n2. **Targeted Therapy**: PARP inhibitors (Olaparib, Talazoparib) leverage synthetic lethality to target HRD cells.\n3. **Chemotherapy Selection**: Conveys high sensitivity to platinum-based doublets (carboplatin, cisplatin).\n4. **Trials**: Screen for phase II/III trials evaluating PARP inhibitor combinations (e.g., with anti-VEGF).";
      } else if (q.includes("immunotherapy") || q.includes("checkpoint")) {
        fallbackResponse = "🛡️ **Cancer Immunotherapy Guide**:\n\n1. **Mechanism**: Blocks PD-1 (Pembrolizumab, Nivolumab), PD-L1 (Atezolizumab), or CTLA-4 (Ipilimumab) to reactivate T-cell anti-tumor responses.\n2. **Biomarkers**: PD-L1 Tumor Proportion Score (TPS), Microsatellite Instability-High (MSI-H), and Tumor Mutational Burden (TMB) predict response.\n3. **Toxicity**: Monitor for immune-related adverse events (colitis, pneumonitis, thyroiditis) requiring steroids.";
      } else if (q.includes("trial") || q.includes("study")) {
        fallbackResponse = "🧪 **Clinical Trial Matching Protocol**:\n\n1. **Inclusion Criteria**: Verify cancer stage, biomarker profile, and previous therapy lines.\n2. **ECOG Status**: Standard trials require ECOG 0 or 1 performance status; ECOG 2+ requires special protocols.\n3. **Phase Guide**: Phase I (Safety/Dose), Phase II (Efficacy), Phase III (Comparison with standard care).\n4. **Action**: Query ClinicalTrials.gov using NCT identifiers and cross-check exclusion criteria.";
      } else {
        fallbackResponse = "🩺 **OncoAgent Clinical Assistant**:\n\nWelcome! I am OncoAgent, your oncology research AI companion. I can assist with queries on:\n- **Targeted Genomics** (e.g., EGFR, BRCA1/2, KRAS, ALK)\n- **Clinical Trial Matching** & eligibility criteria (ECOG status)\n- **Immunotherapies** and molecular checkpoint inhibitors\n\nHow can I assist your clinical search or case analysis today?";
      }

      // Simulate a small network delay for fallback
      setTimeout(() => {
        setMessages(prev => [...prev, {
          id: `assistant-${++messageIdCounter.current}`,
          role: "assistant",
          content: fallbackResponse
        }]);
        setIsLoading(false);
      }, 800);
      return;
    }

    setIsLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setInputValue("");
  };

  // Render markdown-like bold markers and lists cleanly
  const renderFormattedContent = (text: string) => {
    const lines = text.split("\n");
    return lines.map((line, idx) => {
      const content = line;
      
      // Parse bold **tags**
      const boldRegex = /\*\*(.*?)\*\*/g;
      const parts = [];
      let lastIndex = 0;
      let match;
      
      while ((match = boldRegex.exec(content)) !== null) {
        if (match.index > lastIndex) {
          parts.push(content.substring(lastIndex, match.index));
        }
        parts.push(<strong key={match.index}>{match[1]}</strong>);
        lastIndex = boldRegex.lastIndex;
      }
      
      if (lastIndex < content.length) {
        parts.push(content.substring(lastIndex));
      }

      const isList = line.startsWith("- ") || line.match(/^\d+\.\s/);

      return (
        <div key={idx} style={{ 
          marginBottom: line.trim() === "" ? "0.8rem" : "0.3rem",
          paddingLeft: isList ? "1rem" : "0",
          textIndent: isList ? "-1rem" : "0"
        }}>
          {parts.length > 0 ? parts : line}
        </div>
      );
    });
  };

  const suggestions = [
    {
      title: "EGFR Lung Mutation",
      desc: "What is the standard first-line therapy for EGFR-mutated NSCLC?",
      query: "What is the standard first-line therapy for EGFR-mutated NSCLC?"
    },
    {
      title: "BRCA Breast Cancer",
      desc: "Explain how PARP inhibitors target BRCA-mutated breast cancer.",
      query: "Explain how PARP inhibitors target BRCA-mutated breast cancer."
    },
    {
      title: "Immunotherapy Biomarkers",
      desc: "Which biomarkers predict a patient's response to immunotherapy?",
      query: "Which biomarkers predict a patient's response to immunotherapy?"
    },
    {
      title: "Clinical Trial Protocol",
      desc: "What is the clinical trial protocol search guidelines?",
      query: "What is the clinical trial protocol search guidelines?"
    }
  ];

  return (
    <div className={styles.container}>
      {/* Sidebar */}
       <aside className={`${styles.sidebar} ${!isSidebarOpen ? styles.sidebarClosed : ""}`}>
        <div className={`${styles.sidebarContent} ${!isSidebarOpen ? styles.sidebarContentHidden : ""}`}>
          <div>
            <button className={styles.newChatBtn} onClick={startNewChat}>
              <Plus size={16} />
              <span>New Chat</span>
            </button>
            
            <div className={styles.tabContainer}>
              <button 
                className={`${styles.tabBtn} ${activeTab === "chat" ? styles.activeTabBtn : ""}`} 
                onClick={() => setActiveTab("chat")}
              >
                <MessageSquare size={14} />
                <span>Chat</span>
              </button>
              <button 
                className={`${styles.tabBtn} ${activeTab === "documents" ? styles.activeTabBtn : ""}`} 
                onClick={() => setActiveTab("documents")}
              >
                <BookOpen size={14} />
                <span>Documents</span>
              </button>
            </div>
            
            <div className={styles.historySection}>
              <h4 className={styles.historyTitle}>Recent Clinical Queries</h4>
              {messages.length > 0 && (
                <div className={styles.historyItem} onClick={() => {}}>
                  <MessageSquare size={14} style={{ marginRight: 8, display: "inline" }} />
                  <span>{messages[0].content}</span>
                </div>
              )}
              <div className={styles.historyItem}>
                <MessageSquare size={14} style={{ marginRight: 8, display: "inline" }} />
                <span>EGFR Lung mutation trials</span>
              </div>
              <div className={styles.historyItem}>
                <MessageSquare size={14} style={{ marginRight: 8, display: "inline" }} />
                <span>BRCA1 patient report analysis</span>
              </div>
            </div>
          </div>

          <div className={styles.sidebarFooter}>
            <div className={styles.statusDot}></div>
            <span>OncoAgent: Active</span>
          </div>
        </div>
      </aside>

      {/* Main Workspace */}
      <main className={styles.chatArea}>
        {/* Top Header */}
        <header className={styles.header}>
          <div className={styles.headerTitle}>
            <button 
              className={styles.toggleBtn} 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              title={isSidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
            >
              {isSidebarOpen ? <PanelLeftClose size={18} /> : <PanelLeftOpen size={18} />}
            </button>
            <Sparkles size={16} style={{ color: "#e05e36", marginLeft: 8 }} />
            <span>OncoAgent Chat</span>
            <span className={styles.modelBadge}>Clinical-V2</span>
          </div>
        </header>

        {activeTab === "chat" ? (
          <>
            {/* Message Panel */}
            <div className={styles.messagesList}>
              {messages.length === 0 ? (
                <div className={styles.welcomeContainer}>
                  <div className={styles.welcomeIcon}>Ω</div>
                  <h2 className={styles.welcomeTitle}>I am OncoAgent</h2>
                  <p className={styles.welcomeSubtitle}>
                    A specialized medical advisor companion trained in clinical oncology trial matching, targeted molecular variants, and immunotherapy guidelines.
                  </p>
                  
                  <div className={styles.promptGrid}>
                    {suggestions.map((s, idx) => (
                      <button 
                        key={idx} 
                        className={styles.promptCard}
                        onClick={() => handleSend(s.query)}
                      >
                        <div className={styles.promptCardHeader}>
                          <span className={styles.promptCardTitle}>{s.title}</span>
                          <Sparkles size={12} className={styles.promptCardIcon} />
                        </div>
                        <p className={styles.promptCardDesc}>{s.desc}</p>
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className={styles.messagesContainer}>
                  {messages.map((msg) => (
                    <div 
                      key={msg.id} 
                      className={`${styles.messageWrapper} ${msg.role === "user" ? styles.userWrapper : styles.assistantWrapper}`}
                    >
                      <div className={`${styles.messageBubble} ${msg.role === "user" ? styles.userBubble : styles.assistantBubble}`}>
                        {msg.role === "assistant" && (
                          <div className={styles.assistantBadge}>OncoAgent</div>
                        )}
                        <div className={styles.messageContent}>
                          {msg.role === "user" ? msg.content : renderFormattedContent(msg.content)}
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {isLoading && (
                    <div className={`${styles.messageWrapper} ${styles.assistantWrapper}`}>
                      <div className={`${styles.messageBubble} ${styles.assistantBubble}`}>
                        <div className={styles.assistantBadge}>OncoAgent</div>
                        <div className={styles.typing}>
                          <div className={styles.dot}></div>
                          <div className={styles.dot}></div>
                          <div className={styles.dot}></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              )}
            </div>

            {/* Input box */}
            <div className={styles.inputContainer}>
              <div className={`${styles.inputWrapper} ${isFocused ? styles.inputWrapperFocused : ""}`}>
                <textarea
                  ref={textareaRef}
                  className={styles.textarea}
                  placeholder="Ask about lung mutations, clinical trial protocols, immunotherapies..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  onFocus={() => setIsFocused(true)}
                  onBlur={() => setIsFocused(false)}
                  disabled={isLoading}
                  rows={1}
                />
                
                <div className={styles.inputControls}>
                  <button className={styles.attachmentBtn} title="Attach Clinical Notes">
                    <Paperclip size={16} />
                  </button>
                  
                  <button 
                    className={styles.sendBtn} 
                    onClick={() => handleSend()}
                    disabled={isLoading || !inputValue.trim()}
                  >
                    <Send size={14} />
                  </button>
                </div>
              </div>
            </div>
          </>
        ) : (
          /* Document Center Tab */
          <div className={styles.docCenter}>
            <div className={styles.docHeader}>
              <h2 className={styles.docTitle}>Document Center</h2>
              <p className={styles.docSubtitle}>
                Upload clinical papers, molecular reports, or patient cohorts to index in the RAG vector storage.
              </p>
            </div>

            {/* Dropzone */}
            <div className={styles.dropzone} onClick={() => fileInputRef.current?.click()}>
              <input 
                type="file" 
                ref={fileInputRef} 
                style={{ display: "none" }} 
                onChange={handleFileUpload} 
              />
              <div className={styles.dropzoneIcon}>
                {isUploading ? <Loader2 style={{ animation: "spin 1s linear infinite" }} size={24} /> : <UploadCloud size={24} />}
              </div>
              <div>
                <p className={styles.dropzoneText}>
                  {isUploading ? "Uploading to RAG storage..." : "Click to select a file or drag & drop"}
                </p>
                <p className={styles.dropzoneSubtext}>
                  Supports PDF, TXT, MD, DOCX (Max 20MB)
                </p>
              </div>
            </div>

            {uploadMessage && (
              <div style={{ 
                padding: "10px 16px", 
                borderRadius: "8px", 
                backgroundColor: uploadMessage.startsWith("Success") ? "rgba(16, 185, 129, 0.1)" : "rgba(239, 68, 68, 0.1)",
                color: uploadMessage.startsWith("Success") ? "#10b981" : "#ef4444",
                fontSize: "0.85rem",
                fontWeight: 500,
                border: uploadMessage.startsWith("Success") ? "1px solid rgba(16, 185, 129, 0.2)" : "1px solid rgba(239, 68, 68, 0.2)"
              }}>
                {uploadMessage}
              </div>
            )}

            {/* File List */}
            <div className={styles.fileListSection}>
              <h3 className={styles.sectionTitle}>Uploaded Reference Materials</h3>
              {uploadedFiles.length === 0 ? (
                <div className={styles.emptyState}>
                  No documents uploaded yet. Add files above to build your local workspace cache.
                </div>
              ) : (
                <div className={styles.fileList}>
                  {uploadedFiles.map((file, idx) => (
                    <div key={idx} className={styles.fileItem}>
                      <div className={styles.fileInfo}>
                        <FileText size={18} className={styles.fileIcon} />
                        <span className={styles.fileName}>{file.name}</span>
                        <span style={{ 
                          fontSize: "0.7rem", 
                          color: "#8a8a85",
                          backgroundColor: "#262625",
                          padding: "2px 8px",
                          borderRadius: "4px",
                          marginLeft: "12px",
                          textTransform: "uppercase",
                          fontWeight: 600,
                          border: "1px solid #333332"
                        }}>{file.type}</span>
                      </div>
                      <span className={styles.fileStatus}>Ready</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

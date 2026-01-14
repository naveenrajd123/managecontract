/**
 * Frontend JavaScript for Contract Management System
 * This handles all user interactions and API calls
 */

// ============================================================================
// API BASE URL
// ============================================================================
const API_BASE = '';  // Empty since we're on the same server

// ============================================================================
// TAB SWITCHING
// ============================================================================
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all tabs
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked tab
        button.classList.add('active');
        const tabId = button.getAttribute('data-tab') + '-tab';
        document.getElementById(tabId).classList.add('active');
        
        // Load data when switching to contracts tab
        if (button.getAttribute('data-tab') === 'contracts') {
            loadContracts();
        }
        
        // Load contract list for AI questions
        if (button.getAttribute('data-tab') === 'ask') {
            loadContractsForSelect();
        }
    });
});

// ============================================================================
// GLOBAL FILTER STATE
// ============================================================================
let currentFilter = null;

// ============================================================================
// LOAD DASHBOARD STATS
// ============================================================================
async function loadDashboardStats() {
    console.log('[DASHBOARD] Loading dashboard stats...');
    
    try {
        const response = await fetch(`${API_BASE}/api/dashboard/stats`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('[DASHBOARD] Stats received:', data);
        
        // Update status counts with fallback to 0
        document.getElementById('total-count').textContent = data.total_contracts ?? 0;
        document.getElementById('active-count').textContent = data.active_contracts ?? 0;
        document.getElementById('expired-count').textContent = data.expired_contracts ?? 0;
        document.getElementById('renewed-count').textContent = data.renewed_contracts ?? 0;
        document.getElementById('pending-count').textContent = data.pending_contracts ?? 0;
        
        console.log(`[DASHBOARD] Updated stats - Total: ${data.total_contracts}, Active: ${data.active_contracts}`);
        
        // Load warning count
        await loadWarningCount();
        
        // Load risk level stats
        await loadRiskStats();
        
    } catch (error) {
        console.error('[DASHBOARD ERROR] Failed to load dashboard stats:', error);
        
        // Set all to 0 on error so user knows there's an issue
        document.getElementById('total-count').textContent = '?';
        document.getElementById('active-count').textContent = '?';
        document.getElementById('expired-count').textContent = '?';
        document.getElementById('renewed-count').textContent = '?';
        document.getElementById('pending-count').textContent = '?';
        
        // Show error message to user
        console.error('[DASHBOARD ERROR] The server might not be running. Please check if the backend is started.');
    }
}

// ============================================================================
// LOAD WARNING COUNT WITH BREAKDOWN
// ============================================================================
async function loadWarningCount() {
    try {
        const response = await fetch(`${API_BASE}/api/warnings`);
        const data = await response.json();
        
        const warningCount = document.getElementById('warning-count');
        
        // Count unique contracts with warnings (not warning objects)
        const uniqueContracts = new Set();
        data.warnings.forEach(warning => {
            if (warning.contract_id) {
                uniqueContracts.add(warning.contract_id);
            }
        });
        
        const totalContractsWithWarnings = uniqueContracts.size;
        warningCount.textContent = totalContractsWithWarnings;
        
        // Store warning data for breakdown
        window.warningData = {
            critical: data.stats.critical_count,
            warning: data.stats.warning_count,
            info: data.stats.info_count,
            total: totalContractsWithWarnings,
            totalWarnings: data.warnings.length,
            warnings: data.warnings
        };
        
        // Add tooltip with breakdown
        const warningCard = document.getElementById('stat-card-warning');
        if (warningCard) {
            warningCard.title = `${totalContractsWithWarnings} contracts with warnings\nCritical: ${data.stats.critical_count} | Warning: ${data.stats.warning_count} | Info: ${data.stats.info_count}`;
        }
        
        console.log(`[INFO] Found ${totalContractsWithWarnings} contracts with ${data.warnings.length} total warnings`);
        console.log('[INFO] Warning breakdown:', data.stats);
        
    } catch (error) {
        console.error('Error loading warning count:', error);
        document.getElementById('warning-count').textContent = '0';
    }
}

// ============================================================================
// LOAD RISK LEVEL STATS
// ============================================================================
async function loadRiskStats() {
    try {
        const response = await fetch(`${API_BASE}/api/contracts`);
        const contracts = await response.json();
        
        // Count by risk level
        const riskCounts = {
            low: 0,
            medium: 0,
            high: 0,
            critical: 0
        };
        
        contracts.forEach(contract => {
            const risk = contract.risk_level ? contract.risk_level.toLowerCase() : 'low';
            if (riskCounts.hasOwnProperty(risk)) {
                riskCounts[risk]++;
            }
        });
        
        // Update risk stat cards
        document.getElementById('risk-low-count').textContent = riskCounts.low;
        document.getElementById('risk-medium-count').textContent = riskCounts.medium;
        document.getElementById('risk-high-count').textContent = riskCounts.high;
        document.getElementById('risk-critical-count').textContent = riskCounts.critical;
        
    } catch (error) {
        console.error('Error loading risk stats:', error);
        document.getElementById('risk-low-count').textContent = '0';
        document.getElementById('risk-medium-count').textContent = '0';
        document.getElementById('risk-high-count').textContent = '0';
        document.getElementById('risk-critical-count').textContent = '0';
    }
}

// ============================================================================
// LOAD CRITICAL COUNT (kept for backward compatibility)
// ============================================================================
async function loadCriticalCount() {
    try {
        const response = await fetch(`${API_BASE}/api/warnings`);
        const data = await response.json();
        
        const criticalCount = document.getElementById('critical-count');
        
        // Count critical contracts (warnings)
        const totalCritical = data.stats.critical_count + data.stats.warning_count;
        criticalCount.textContent = totalCritical;
        
    } catch (error) {
        console.error('Error loading critical count:', error);
        document.getElementById('critical-count').textContent = '0';
    }
}

// ============================================================================
// LOAD WARNINGS (kept for backward compatibility, but not displayed on homepage)
// ============================================================================
async function loadWarnings() {
    try {
        const response = await fetch(`${API_BASE}/api/warnings`);
        const data = await response.json();
        
        const warningsContainer = document.getElementById('warnings-container');
        const warningCount = document.getElementById('warning-count');
        
        if (data.warnings.length === 0) {
            warningsContainer.innerHTML = '<p class="loading">✅ No warnings! All contracts are in good standing.</p>';
            warningCount.textContent = '0';
            return;
        }
        
        warningCount.textContent = data.stats.critical_count + data.stats.warning_count;
        
        // Display warnings
        warningsContainer.innerHTML = data.warnings.map(warning => `
            <div class="warning-card ${warning.severity}">
                <div class="warning-info">
                    <h4>${warning.contract_name}</h4>
                    <p>${warning.message}</p>
                    <small>Contract #${warning.contract_number}</small>
                </div>
                <div class="warning-badge ${warning.severity}">
                    ${warning.severity}
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading warnings:', error);
        document.getElementById('warnings-container').innerHTML = '<p class="loading">Error loading warnings</p>';
    }
}

// ============================================================================
// LOAD CONTRACTS
// ============================================================================
async function loadContracts(filterType = null) {
    const statusFilter = filterType || document.getElementById('status-filter').value;
    const contractsContainer = document.getElementById('contracts-container');
    
    // Store the current filter
    currentFilter = filterType;
    
    contractsContainer.innerHTML = '<p class="loading">Loading contracts...</p>';
    
    try {
        let url = `${API_BASE}/api/contracts`;
        
        // Only add status filter for actual status values, not for warning/risk filters
        const validStatuses = ['active', 'expired', 'renewed', 'pending'];
        if (statusFilter && statusFilter !== 'all' && validStatuses.includes(statusFilter)) {
            url += `?status=${statusFilter}`;
        }
        
        console.log(`[INFO] Fetching contracts from: ${url}`);
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        let contracts = await response.json();
        console.log(`[INFO] Received ${contracts.length} contracts from API`);
        
        // Validate that we got an array
        if (!Array.isArray(contracts)) {
            console.error('[ERROR] API returned invalid data (not an array):', contracts);
            throw new Error('Invalid data format from server');
        }
        
        // Apply additional filtering for critical/warnings
        if (filterType === 'critical' || filterType === 'warnings') {
            const beforeCount = contracts.length;
            contracts = contracts.filter(contract => {
                // Only show ACTIVE contracts for warnings (matches early warning system logic)
                if (contract.status !== 'active') {
                    return false;
                }
                
                const endDate = new Date(contract.end_date);
                const today = new Date();
                const daysUntilExpiry = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));
                
                // Include active contracts expiring in 180 days or high/critical risk
                const riskLevel = contract.risk_level ? contract.risk_level.toLowerCase() : '';
                const isHighRisk = riskLevel === 'high' || riskLevel === 'critical';
                
                // Match early warning system logic: expiration within 180 days OR high/critical risk
                const hasWarning = daysUntilExpiry <= 180 || isHighRisk || daysUntilExpiry < 0;
                
                // Debug logging
                if (hasWarning) {
                    console.log(`[WARNING] Contract ${contract.contract_number}:`, {
                        status: contract.status,
                        daysUntilExpiry,
                        riskLevel,
                        isHighRisk
                    });
                }
                
                return hasWarning;
            });
            console.log(`[INFO] Warning filter: ${beforeCount} total contracts → ${contracts.length} with warnings`);
        }
        
        // Apply risk level filtering
        if (filterType === 'risk-low') {
            contracts = contracts.filter(contract => 
                contract.risk_level && contract.risk_level.toLowerCase() === 'low'
            );
        } else if (filterType === 'risk-medium') {
            contracts = contracts.filter(contract => 
                contract.risk_level && contract.risk_level.toLowerCase() === 'medium'
            );
        } else if (filterType === 'risk-high') {
            contracts = contracts.filter(contract => 
                contract.risk_level && contract.risk_level.toLowerCase() === 'high'
            );
        } else if (filterType === 'risk-critical') {
            contracts = contracts.filter(contract => 
                contract.risk_level && contract.risk_level.toLowerCase() === 'critical'
            );
        }
        
        if (contracts.length === 0) {
            let filterMessage = 'No contracts found. Upload your first contract!';
            
            if (filterType === 'critical') {
                filterMessage = 'No critical contracts found!';
            } else if (filterType === 'warnings') {
                filterMessage = `
                    <div style="text-align: center; padding: 40px;">
                        <div style="font-size: 3rem; margin-bottom: 20px;">✅</div>
                        <h3 style="color: #27ae60; margin-bottom: 15px;">No Warning Contracts Found!</h3>
                        <p style="color: #666; margin-bottom: 20px;">All active contracts are in good standing.</p>
                        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #3498db; text-align: left; max-width: 600px; margin: 0 auto;">
                            <strong style="color: #1e3a5f;">Warning Criteria:</strong>
                            <ul style="margin-top: 10px; line-height: 1.8; color: #555;">
                                <li>🔴 <strong>Critical:</strong> Expiring within 30 days</li>
                                <li>🟡 <strong>Warning:</strong> Expiring within 90 days</li>
                                <li>🔵 <strong>Info:</strong> Expiring within 180 days</li>
                                <li>⚠️ <strong>Risk:</strong> High or Critical risk level</li>
                            </ul>
                            <p style="margin-top: 15px; font-style: italic; color: #666; font-size: 0.9em;">
                                Note: Warnings are only calculated for <strong>active</strong> contracts.
                            </p>
                        </div>
                    </div>
                `;
            } else if (filterType === 'risk-low') {
                filterMessage = 'No LOW risk contracts found!';
            } else if (filterType === 'risk-medium') {
                filterMessage = 'No MEDIUM risk contracts found!';
            } else if (filterType === 'risk-high') {
                filterMessage = 'No HIGH risk contracts found!';
            } else if (filterType === 'risk-critical') {
                filterMessage = 'No CRITICAL risk contracts found!';
            }
            
            contractsContainer.innerHTML = `<div class="loading">${filterMessage}</div>`;
            return;
        }
        
        // Add warning breakdown header if showing warnings
        let headerHTML = '';
        if (filterType === 'warnings' && contracts.length > 0) {
            // Calculate warning counts by category
            const today = new Date();
            const warningCounts = {
                critical: 0,
                warning: 0,
                info: 0,
                risk: 0
            };
            
            contracts.forEach(contract => {
                const endDate = new Date(contract.end_date);
                const daysUntilExpiry = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));
                const riskLevel = contract.risk_level ? contract.risk_level.toLowerCase() : '';
                
                if (daysUntilExpiry <= 30 && daysUntilExpiry >= 0) {
                    warningCounts.critical++;
                } else if (daysUntilExpiry <= 90 && daysUntilExpiry > 30) {
                    warningCounts.warning++;
                } else if (daysUntilExpiry <= 180 && daysUntilExpiry > 90) {
                    warningCounts.info++;
                } else if (daysUntilExpiry < 0) {
                    warningCounts.critical++; // Expired
                }
                
                if (riskLevel === 'high' || riskLevel === 'critical') {
                    warningCounts.risk++;
                }
            });
            
            headerHTML = `
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;">
                    <h3 style="margin-bottom: 15px; display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 2rem;">⚠️</span>
                        <span>Warning Contracts (${contracts.length} Active Contracts)</span>
                        <button onclick="loadContracts('warnings')" style="margin-left: auto; background: rgba(255,255,255,0.3); color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 0.9rem; font-weight: 600;">
                            🔄 Show All Warnings
                        </button>
                    </h3>
                    <p style="margin-bottom: 15px; opacity: 0.95;">These active contracts need attention. Click on a category below to filter:</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin-top: 15px;">
                        <div onclick="filterWarningsByCategory('critical')" style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px); cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.transform='scale(1.05)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='scale(1)'">
                            <div style="font-size: 1.8rem; font-weight: bold;">${warningCounts.critical}</div>
                            <div style="font-size: 1.2rem; margin-bottom: 5px;">🔴 Critical</div>
                            <div style="font-size: 0.85rem; opacity: 0.9;">Expiring ≤ 30 days or Expired</div>
                            <div style="font-size: 0.75rem; margin-top: 8px; opacity: 0.8; font-style: italic;">Click to filter</div>
                        </div>
                        <div onclick="filterWarningsByCategory('warning')" style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px); cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.transform='scale(1.05)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='scale(1)'">
                            <div style="font-size: 1.8rem; font-weight: bold;">${warningCounts.warning}</div>
                            <div style="font-size: 1.2rem; margin-bottom: 5px;">🟡 Warning</div>
                            <div style="font-size: 0.85rem; opacity: 0.9;">Expiring 31-90 days</div>
                            <div style="font-size: 0.75rem; margin-top: 8px; opacity: 0.8; font-style: italic;">Click to filter</div>
                        </div>
                        <div onclick="filterWarningsByCategory('info')" style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px); cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.transform='scale(1.05)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='scale(1)'">
                            <div style="font-size: 1.8rem; font-weight: bold;">${warningCounts.info}</div>
                            <div style="font-size: 1.2rem; margin-bottom: 5px;">🔵 Info</div>
                            <div style="font-size: 0.85rem; opacity: 0.9;">Expiring 91-180 days</div>
                            <div style="font-size: 0.75rem; margin-top: 8px; opacity: 0.8; font-style: italic;">Click to filter</div>
                        </div>
                        <div onclick="filterWarningsByCategory('risk')" style="background: rgba(255,255,255,0.2); padding: 12px; border-radius: 8px; backdrop-filter: blur(10px); cursor: pointer; transition: all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.transform='scale(1.05)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'; this.style.transform='scale(1)'">
                            <div style="font-size: 1.8rem; font-weight: bold;">${warningCounts.risk}</div>
                            <div style="font-size: 1.2rem; margin-bottom: 5px;">⚠️ Risk</div>
                            <div style="font-size: 0.85rem; opacity: 0.9;">High/Critical Risk</div>
                            <div style="font-size: 0.75rem; margin-top: 8px; opacity: 0.8; font-style: italic;">Click to filter</div>
                        </div>
                    </div>
                </div>
            `;
        }
        
        contractsContainer.innerHTML = headerHTML + contracts.map(contract => {
            const startDate = new Date(contract.start_date).toLocaleDateString();
            const endDate = new Date(contract.end_date).toLocaleDateString();
            const value = contract.contract_value 
                ? new Intl.NumberFormat('en-US', { style: 'currency', currency: contract.currency }).format(contract.contract_value)
                : 'N/A';
            
            const summaryId = `summary-${contract.id}`;
            const hasFullSummary = contract.summary && contract.summary.length > 200;
            
            // Calculate warning indicators if viewing warnings
            let warningBadge = '';
            if (filterType === 'warnings') {
                const endDateObj = new Date(contract.end_date);
                const today = new Date();
                const daysUntilExpiry = Math.ceil((endDateObj - today) / (1000 * 60 * 60 * 24));
                const riskLevel = contract.risk_level ? contract.risk_level.toLowerCase() : '';
                
                let warningType = '';
                let warningIcon = '';
                let warningColor = '';
                
                if (daysUntilExpiry <= 30 && daysUntilExpiry > 0) {
                    warningType = 'Critical - Expires in ' + daysUntilExpiry + ' days';
                    warningIcon = '🔴';
                    warningColor = '#e74c3c';
                } else if (daysUntilExpiry <= 90 && daysUntilExpiry > 30) {
                    warningType = 'Warning - Expires in ' + daysUntilExpiry + ' days';
                    warningIcon = '🟡';
                    warningColor = '#f39c12';
                } else if (daysUntilExpiry <= 180 && daysUntilExpiry > 90) {
                    warningType = 'Info - Expires in ' + daysUntilExpiry + ' days';
                    warningIcon = '🔵';
                    warningColor = '#3498db';
                } else if (daysUntilExpiry < 0) {
                    warningType = 'Expired ' + Math.abs(daysUntilExpiry) + ' days ago';
                    warningIcon = '🔴';
                    warningColor = '#c0392b';
                }
                
                if (riskLevel === 'high' || riskLevel === 'critical') {
                    if (warningType) warningType += ' + ';
                    warningType += 'High Risk';
                    warningIcon += ' ⚠️';
                }
                
                if (warningType) {
                    warningBadge = `
                        <div style="background: ${warningColor}; color: white; padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; display: inline-block;">
                            ${warningIcon} ${warningType}
                        </div>
                    `;
                }
            }
            
            return `
                <div class="contract-card" data-contract-id="${contract.id}">
                    ${warningBadge}
                    <div class="contract-header">
                        <div>
                            <div class="contract-title">${contract.contract_name}</div>
                            <div class="contract-number">Contract #${contract.contract_number}</div>
                        </div>
                        <div class="contract-status ${contract.status}">${contract.status}</div>
                    </div>
                    
                    <div class="contract-details">
                        <div class="detail-item">
                            <span class="detail-label">Party A:</span> ${contract.party_a || 'N/A'}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Party B:</span> ${contract.party_b || 'N/A'}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Start Date:</span> ${startDate}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">End Date:</span> ${endDate}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Value:</span> ${value}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Risk Level:</span> 
                            <div style="display: inline-block;">
                                <span style="text-transform: uppercase; font-weight: bold; color: ${getRiskColor(contract.risk_level)}">${contract.risk_level}</span>
                                ${contract.risk_reason ? 
                                    `<div style="font-size: 0.8rem; color: #666; font-style: italic; margin-top: 3px;">💡 ${contract.risk_reason}</div>` : 
                                    `<button onclick="reanalyzeContract(${contract.id})" style="background: #3498db; color: white; border: none; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; margin-left: 8px; font-weight: 600;">
                                        🔄 Get AI Reason
                                    </button>`
                                }
                            </div>
                        </div>
                    </div>
                    
                    ${contract.summary ? `
                        <div class="contract-summary-section">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <strong style="color: #1e3a5f; font-size: 1.1em;">🤖 AI-Generated Analysis</strong>
                                ${hasFullSummary ? `
                                    <button class="btn-expand" onclick="toggleSummary('${summaryId}')" style="background: #2c5f7c; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 0.9em;">
                                        <span id="${summaryId}-btn-text">Show Full Analysis</span>
                                    </button>
                                ` : ''}
                            </div>
                            <div id="${summaryId}" class="contract-summary-content" style="display: ${hasFullSummary ? 'none' : 'block'}; max-height: none; overflow: hidden; background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #2c5f7c;">
                                ${formatSummary(contract.summary)}
                            </div>
                            ${hasFullSummary ? `
                                <div id="${summaryId}-preview" class="contract-summary-preview" style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #2c5f7c; color: #555;">
                                    ${contract.summary.substring(0, 200)}... <em style="color: #2c5f7c;">(Click "Show Full Analysis" to see complete details)</em>
                                </div>
                            ` : ''}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Error loading contracts:', error);
        contractsContainer.innerHTML = '<p class="loading">Error loading contracts</p>';
    }
}

function getRiskColor(riskLevel) {
    const colors = {
        'low': '#27ae60',
        'medium': '#f39c12',
        'high': '#e74c3c',
        'critical': '#c0392b'
    };
    return colors[riskLevel] || '#666';
}

// Format summary text with hierarchical structure (main sections and subsections)
function formatSummary(text) {
    if (!text) return '';
    
    // Convert markdown bold (**text**) to HTML bold
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    let lines = text.split('\n');
    let html = '';
    let inList = false;
    let currentIndent = 0;
    
    for (let line of lines) {
        // Measure indentation (count leading spaces)
        const indent = line.search(/\S/);
        const trimmedLine = line.trim();
        
        if (trimmedLine.length === 0) continue;
        
        // Detect main section headers (usually in BOLD CAPS or just bold)
        const isMainSection = trimmedLine.match(/^<strong>[A-Z\s&]+<\/strong>$/);
        
        // Detect subsection headers (bold text with colon)
        const isSubSection = trimmedLine.match(/^<strong>.*:<\/strong>$/);
        
        // Detect bullet points
        const isBullet = trimmedLine.match(/^[\*\-•]\s+/);
        
        if (isMainSection) {
            // Close any open list
            if (inList) {
                html += '</ul>';
                inList = false;
            }
            // Main section header with prominent styling
            html += `<h3 style="color: #1e3a5f; margin-top: 25px; margin-bottom: 10px; font-size: 1.1em; border-bottom: 2px solid #2c5f7c; padding-bottom: 5px;">${trimmedLine}</h3>`;
        } else if (isSubSection) {
            // Close any open list
            if (inList) {
                html += '</ul>';
                inList = false;
            }
            // Subsection header with moderate styling
            html += `<h4 style="color: #2c5f7c; margin-top: 15px; margin-bottom: 8px; margin-left: 15px; font-size: 1em;">${trimmedLine}</h4>`;
        } else if (isBullet) {
            // Start list if not already in one
            if (!inList) {
                const marginLeft = indent > 0 ? '30px' : '15px';
                html += `<ul style="margin: 5px 0; padding-left: 20px; margin-left: ${marginLeft}; list-style-type: disc;">`;
                inList = true;
            }
            // Remove bullet and add as list item
            let content = trimmedLine.replace(/^[\*\-•]\s+/, '');
            html += `<li style="margin: 5px 0; line-height: 1.6;">${content}</li>`;
        } else {
            // Regular paragraph
            if (inList) {
                html += '</ul>';
                inList = false;
            }
            html += `<p style="margin: 10px 0 10px 15px;">${trimmedLine}</p>`;
        }
    }
    
    // Close any remaining open list
    if (inList) {
        html += '</ul>';
    }
    
    return html;
}

// ============================================================================
// FILE UPLOAD - DRAG & DROP AND FILE SELECTION
// ============================================================================

// Show file name(s) when selected
document.getElementById('contract-file').addEventListener('change', (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        if (files.length === 1) {
            document.getElementById('file-name').textContent = `Selected: ${files[0].name}`;
        } else {
            document.getElementById('file-name').textContent = `Selected: ${files.length} files`;
        }
    }
});

// Drag and drop functionality
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('contract-file');

// Click to upload
uploadArea.addEventListener('click', (e) => {
    // Only trigger if clicking the area itself, not if a button was clicked
    if (e.target === uploadArea || uploadArea.contains(e.target)) {
        fileInput.click();
    }
});

// Drag over
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

// Drag leave
uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

// Drop file
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        // Set all files to the input
        fileInput.files = files;
        if (files.length === 1) {
            document.getElementById('file-name').textContent = `Selected: ${files[0].name}`;
        } else {
            document.getElementById('file-name').textContent = `Selected: ${files.length} files`;
        }
    }
});

// ============================================================================
// UPLOAD CONTRACT FORM - SUPPORTS SINGLE AND BULK UPLOAD
// ============================================================================
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('contract-file');
    const files = Array.from(fileInput.files);
    
    if (files.length === 0) {
        alert('Please select at least one file to upload');
        return;
    }
    
    // Check if bulk upload
    if (files.length > 1) {
        await handleBulkUpload(files);
        return;
    }
    
    // Single file upload (existing logic)
    const formData = new FormData();
    formData.append('file', files[0]);
    
    const resultBox = document.getElementById('upload-result');
    resultBox.style.display = 'block';
    resultBox.className = 'result-box';
    
    // Animated progress indicator
    let dots = 0;
    resultBox.innerHTML = `
        <h3 id="processing-header">⏳ Processing Contract<span id="dots"></span></h3>
        <div style="width: 100%; background: #e0e0e0; border-radius: 10px; height: 25px; margin: 15px 0; overflow: hidden;">
            <div id="progress-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); transition: width 0.5s; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 12px;"></div>
        </div>
        <p style="font-size: 14px; color: #666;">Please wait while AI analyzes your document...</p>
        <ul style="text-align: left; margin-top: 15px; line-height: 2; color: #555;">
            <li id="step-1">📄 Extracting text from document...</li>
            <li id="step-2">🔍 Identifying contract details...</li>
            <li id="step-3">🤖 Generating summary...</li>
            <li id="step-4">⚖️ Assessing risk level...</li>
            <li id="step-5">💾 Saving to database...</li>
        </ul>
    `;
    
    // Animate dots
    const dotsInterval = setInterval(() => {
        dots = (dots + 1) % 4;
        const dotsEl = document.getElementById('dots');
        if (dotsEl) dotsEl.textContent = '.'.repeat(dots);
    }, 500);
    
    // Animate progress bar
    const progressBar = document.getElementById('progress-bar');
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress = Math.min(progress + 2, 90); // Max 90% until complete
        progressBar.style.width = progress + '%';
        progressBar.textContent = progress + '%';
    }, 600);
    
    try {
        const response = await fetch(`${API_BASE}/api/contracts/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        // Stop animations
        clearInterval(dotsInterval);
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        progressBar.textContent = '100%';
        
        if (response.ok) {
            resultBox.className = 'result-box success';
            resultBox.innerHTML = `
                <h3>✅ Contract Successfully Processed!</h3>
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <p><strong>📝 Contract Name:</strong> ${result.contract_name}</p>
                    <p><strong>🔢 Contract Number:</strong> ${result.contract_number}</p>
                    <p><strong>🏢 Party A:</strong> ${result.party_a}</p>
                    <p><strong>🏢 Party B:</strong> ${result.party_b}</p>
                    <p><strong>📅 Start Date:</strong> ${new Date(result.start_date).toLocaleDateString()}</p>
                    <p><strong>📅 End Date:</strong> ${new Date(result.end_date).toLocaleDateString()}</p>
                    <p><strong>📊 Status:</strong> <span style="text-transform: uppercase; font-weight: bold;">${result.status}</span></p>
                    <p><strong>⚠️ Risk Level:</strong> <span style="color: ${getRiskColor(result.risk_level)}; font-weight: bold; text-transform: uppercase;">${result.risk_level}</span></p>
                    ${result.risk_reason ? `<p style="margin-left: 20px; font-size: 0.9rem; color: #666; font-style: italic;">💡 ${result.risk_reason}</p>` : ''}
                </div>
                <div style="margin-top: 15px; padding: 15px; background: #f9f9f9; border-radius: 8px;">
                    <strong>🤖 AI-Generated Summary:</strong><br><br>
                    <div style="line-height: 1.8;">${formatSummary(result.summary)}</div>
                </div>
                <p style="margin-top: 15px; color: #27ae60; font-weight: bold;">
                    Contract has been added to your dashboard and is now searchable!
                </p>
            `;
            
            // Reset form
            document.getElementById('upload-form').reset();
            document.getElementById('file-name').textContent = '';
            
            // Reload dashboard
            loadDashboardStats();
            loadWarnings();
            
        } else {
            throw new Error(result.detail || 'Upload failed');
        }
        
    } catch (error) {
        // Stop animations
        clearInterval(dotsInterval);
        clearInterval(progressInterval);
        
        resultBox.className = 'result-box error';
        
        // Check for specific errors
        const errorMsg = error.message.toLowerCase();
        if (errorMsg.includes('unique') || errorMsg.includes('duplicate') || errorMsg.includes('already exists')) {
            resultBox.innerHTML = `
                <h3>⚠️ Duplicate Contract</h3>
                <p>This contract has already been uploaded to the database.</p>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                    Contract number already exists. Please upload a different contract or delete the existing one first.
                </p>
                <p style="margin-top: 10px;">
                    <strong>Tip:</strong> Go to the "All Contracts" tab to view or manage existing contracts.
                </p>
            `;
        } else {
            resultBox.innerHTML = `
                <h3>❌ Upload Error</h3>
                <p>${error.message}</p>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                    Make sure your file is a valid PDF or TXT document with readable text.
                </p>
            `;
        }
    }
});

// ============================================================================
// ASK AI FORM
// ============================================================================
async function loadContractsForSelect() {
    try {
        const response = await fetch(`${API_BASE}/api/contracts`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const contracts = await response.json();
        
        const select = document.getElementById('contract-select');
        if (!select) {
            console.error('Contract select element not found');
            return;
        }
        
        // Clear and reset dropdown
        select.innerHTML = '<option value="">All Contracts</option>';
        
        console.log(`Loading ${contracts.length} contracts into dropdown`);
        
        // Add each contract to the dropdown
        contracts.forEach(contract => {
            const option = document.createElement('option');
            option.value = contract.id;
            option.textContent = `${contract.contract_name || 'Unnamed'} (#${contract.contract_number || 'N/A'})`;
            select.appendChild(option);
        });
        
        console.log(`Successfully loaded ${contracts.length} contracts into dropdown`);
        
        // Initialize chat history for the default "All Contracts" view
        if (!chatHistories['all']) {
            loadChatHistory('');
        }
        
    } catch (error) {
        console.error('Error loading contracts for select:', error);
        const select = document.getElementById('contract-select');
        if (select) {
            select.innerHTML = '<option value="">All Contracts (Error loading list)</option>';
        }
    }
}

// Chat History Management - Store separate conversations for each contract
const chatHistories = {};
let currentContractId = ''; // '' means "All Contracts"

function getCurrentChatKey() {
    return currentContractId || 'all';
}

function saveChatHistory() {
    const chatKey = getCurrentChatKey();
    const chatMessages = document.getElementById('chat-messages');
    chatHistories[chatKey] = chatMessages.innerHTML;
}

function loadChatHistory(contractId) {
    const chatKey = contractId || 'all';
    const chatMessages = document.getElementById('chat-messages');
    
    if (chatHistories[chatKey]) {
        // Load existing chat history for this contract
        chatMessages.innerHTML = chatHistories[chatKey];
        scrollToBottom();
    } else {
        // Fresh chat - show welcome message
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="ai-avatar">🤖</div>
                <div class="message-content">
                    <strong>AI Assistant</strong>
                    <p>Hello! I'm your Contract Management AI Assistant. Ask me anything about ${contractId ? 'this contract' : 'your contracts'}!</p>
                    <p class="help-examples">
                        <strong>Try asking:</strong><br>
                        • "What are the payment terms?"<br>
                        • "Which contracts expire soon?"<br>
                        • "What are the termination clauses?"<br>
                        • "Who are the key stakeholders?"
                    </p>
                </div>
            </div>
        `;
    }
}

function switchContract(newContractId) {
    // Save current chat history before switching
    saveChatHistory();
    
    // Update current contract
    currentContractId = newContractId;
    
    // Load chat history for new contract
    loadChatHistory(newContractId);
}

// Chat Interface Functions
function addUserMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'user-message';
    messageDiv.innerHTML = `
        <div class="user-message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addAIMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'ai-message';
    messageDiv.innerHTML = `
        <div class="ai-avatar">🤖</div>
        <div class="ai-message-content">
            ${formatAIResponse(message)}
        </div>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function showThinkingIndicator() {
    const chatMessages = document.getElementById('chat-messages');
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'ai-thinking';
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.innerHTML = `
        <div class="ai-avatar">🤖</div>
        <div class="thinking-content">
            <div class="thinking-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(thinkingDiv);
    scrollToBottom();
}

function removeThinkingIndicator() {
    const thinkingIndicator = document.getElementById('thinking-indicator');
    if (thinkingIndicator) {
        thinkingIndicator.remove();
    }
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatAIResponse(text) {
    // Convert newlines to <br> and preserve formatting
    let formatted = escapeHtml(text).replace(/\n/g, '<br>');
    
    // Make **text** bold
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert bullet points
    formatted = formatted.replace(/^- (.*?)$/gm, '• $1');
    formatted = formatted.replace(/^\* (.*?)$/gm, '• $1');
    
    return `<p>${formatted}</p>`;
}

// Auto-resize textarea as user types
const questionInput = document.getElementById('question');

questionInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

// Handle Enter key for sending (Shift+Enter for new line)
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('ask-form').dispatchEvent(new Event('submit'));
    }
});

// Handle contract selection change - switch to that contract's chat history
document.getElementById('contract-select').addEventListener('change', (e) => {
    const newContractId = e.target.value;
    switchContract(newContractId);
});

// Ask AI Form Handler
document.getElementById('ask-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    const contractId = document.getElementById('contract-select').value;
    
    if (!question) return;
    
    // Add user message to chat
    addUserMessage(question);
    
    // Clear input immediately and reset height
    questionInput.value = '';
    questionInput.style.height = 'auto';
    
    // Show thinking indicator
    showThinkingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/api/contracts/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                contract_id: contractId ? parseInt(contractId) : null
            })
        });
        
        const result = await response.json();
        
        // Remove thinking indicator
        removeThinkingIndicator();
        
        if (response.ok) {
            // Add AI response to chat
            addAIMessage(result.answer);
            // Save chat history after successful response
            saveChatHistory();
        } else {
            throw new Error(result.detail || 'Failed to get answer');
        }
        
    } catch (error) {
        removeThinkingIndicator();
        addAIMessage(`❌ Sorry, I encountered an error: ${error.message}`);
        // Save chat history even after error
        saveChatHistory();
    }
});

// ============================================================================
// STATUS FILTER
// ============================================================================
document.getElementById('status-filter').addEventListener('change', loadContracts);

// ============================================================================
// BULK UPLOAD HANDLER
// ============================================================================
async function handleBulkUpload(files) {
    const resultBox = document.getElementById('upload-result');
    resultBox.style.display = 'block';
    resultBox.className = 'result-box';
    
    const totalFiles = files.length;
    let successCount = 0;
    let failCount = 0;
    const results = [];
    
    // Show bulk upload progress
    resultBox.innerHTML = `
        <h3>📦 Bulk Upload in Progress</h3>
        <p>Processing ${totalFiles} contracts. Please wait...</p>
        <div style="width: 100%; background: #e0e0e0; border-radius: 10px; height: 30px; margin: 15px 0; overflow: hidden;">
            <div id="bulk-progress-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); transition: width 0.5s; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;"></div>
        </div>
        <div id="bulk-status" style="margin-top: 15px; max-height: 300px; overflow-y: auto; text-align: left;">
            <p style="color: #666;">Starting upload...</p>
        </div>
    `;
    
    const progressBar = document.getElementById('bulk-progress-bar');
    const statusDiv = document.getElementById('bulk-status');
    
    // Process files one by one (sequential to avoid overwhelming the server)
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileNum = i + 1;
        
        // Update status
        statusDiv.innerHTML += `<p style="color: #667eea;">📄 [${fileNum}/${totalFiles}] Processing: ${file.name}...</p>`;
        statusDiv.scrollTop = statusDiv.scrollHeight;
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch(`${API_BASE}/api/contracts/upload`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                successCount++;
                statusDiv.innerHTML += `<p style="color: #27ae60;">✅ [${fileNum}/${totalFiles}] Success: <a href="#" onclick="viewContractMetadata(${result.id}); return false;" style="color: #667eea; font-weight: bold; text-decoration: underline; cursor: pointer;">${result.contract_number} - ${result.contract_name}</a></p>`;
                results.push({success: true, file: file.name, result});
            } else {
                failCount++;
                const errorMsg = result.detail || 'Upload failed';
                statusDiv.innerHTML += `<p style="color: #e74c3c;">❌ [${fileNum}/${totalFiles}] Failed: ${file.name} - ${errorMsg}</p>`;
                results.push({success: false, file: file.name, error: errorMsg});
            }
        } catch (error) {
            failCount++;
            statusDiv.innerHTML += `<p style="color: #e74c3c;">❌ [${fileNum}/${totalFiles}] Error: ${file.name} - ${error.message}</p>`;
            results.push({success: false, file: file.name, error: error.message});
        }
        
        // Update progress bar
        const progress = Math.round(((i + 1) / totalFiles) * 100);
        progressBar.style.width = progress + '%';
        progressBar.textContent = progress + '%';
        
        statusDiv.scrollTop = statusDiv.scrollHeight;
    }
    
    // Show final summary
    resultBox.className = successCount === totalFiles ? 'result-box success' : 
                         failCount === totalFiles ? 'result-box error' : 
                         'result-box';
    
    const summaryHTML = `
        <h3>📊 Bulk Upload Complete</h3>
        <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <p><strong>Total Files:</strong> ${totalFiles}</p>
            <p style="color: #27ae60;"><strong>✅ Successful:</strong> ${successCount}</p>
            <p style="color: #e74c3c;"><strong>❌ Failed:</strong> ${failCount}</p>
        </div>
        <div style="margin-top: 15px; max-height: 400px; overflow-y: auto; text-align: left; background: #f9f9f9; padding: 15px; border-radius: 8px;">
            <strong>Upload Log:</strong><br><br>
            ${statusDiv.innerHTML}
        </div>
        <p style="margin-top: 15px; color: #667eea; font-weight: bold;">
            ${successCount > 0 ? `${successCount} contract(s) added to your dashboard!` : 'No contracts were uploaded.'}
        </p>
    `;
    
    resultBox.innerHTML = summaryHTML;
    
    // Reset form
    document.getElementById('upload-form').reset();
    document.getElementById('file-name').textContent = '';
    
    // Reload dashboard if any succeeded
    if (successCount > 0) {
        loadDashboardStats();
        loadContracts();
    }
}

// ============================================================================
// VIEW CONTRACT METADATA FUNCTION
// ============================================================================
async function viewContractMetadata(contractId) {
    // Switch to contracts tab
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    const contractsBtn = document.querySelector('[data-tab="contracts"]');
    contractsBtn.classList.add('active');
    document.getElementById('contracts-tab').classList.add('active');
    
    // Reset filter and load all contracts
    document.getElementById('status-filter').value = '';
    await loadContracts('all');
    
    // Wait a moment for DOM to update
    setTimeout(() => {
        // Find the contract card
        const contractCard = document.querySelector(`[data-contract-id="${contractId}"]`);
        if (contractCard) {
            // Scroll to the contract
            contractCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Highlight the card temporarily
            contractCard.style.border = '3px solid #667eea';
            contractCard.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.5)';
            
            // Auto-expand the summary if it exists
            const summaryId = `summary-${contractId}`;
            const summaryContent = document.getElementById(summaryId);
            const summaryPreview = document.getElementById(`${summaryId}-preview`);
            const btnText = document.getElementById(`${summaryId}-btn-text`);
            
            if (summaryContent && summaryPreview && btnText) {
                summaryContent.style.display = 'block';
                summaryPreview.style.display = 'none';
                btnText.textContent = 'Hide Full Analysis';
            }
            
            // Remove highlight after 3 seconds
            setTimeout(() => {
                contractCard.style.border = '';
                contractCard.style.boxShadow = '';
            }, 3000);
        }
    }, 500);
}

// Make function globally available
window.viewContractMetadata = viewContractMetadata;

// ============================================================================
// TOGGLE SUMMARY FUNCTION
// ============================================================================
function toggleSummary(summaryId) {
    const summaryContent = document.getElementById(summaryId);
    const summaryPreview = document.getElementById(`${summaryId}-preview`);
    const btnText = document.getElementById(`${summaryId}-btn-text`);
    
    if (summaryContent.style.display === 'none') {
        // Show full summary
        summaryContent.style.display = 'block';
        summaryPreview.style.display = 'none';
        btnText.textContent = 'Hide Full Analysis';
    } else {
        // Show preview
        summaryContent.style.display = 'none';
        summaryPreview.style.display = 'block';
        btnText.textContent = 'Show Full Analysis';
    }
}

// Make function globally available
window.toggleSummary = toggleSummary;

// ============================================================================
// FILTER WARNINGS BY CATEGORY
// ============================================================================
async function filterWarningsByCategory(category) {
    console.log(`[INFO] Filtering warnings by category: ${category}`);
    
    try {
        // Fetch all contracts
        const response = await fetch(`${API_BASE}/api/contracts`);
        let contracts = await response.json();
        
        // Filter to only active contracts
        contracts = contracts.filter(contract => contract.status === 'active');
        
        const today = new Date();
        
        // Filter based on category
        const filteredContracts = contracts.filter(contract => {
            const endDate = new Date(contract.end_date);
            const daysUntilExpiry = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));
            const riskLevel = contract.risk_level ? contract.risk_level.toLowerCase() : '';
            
            switch(category) {
                case 'critical':
                    // Expiring within 30 days or already expired
                    return daysUntilExpiry <= 30;
                    
                case 'warning':
                    // Expiring between 31-90 days
                    return daysUntilExpiry > 30 && daysUntilExpiry <= 90;
                    
                case 'info':
                    // Expiring between 91-180 days
                    return daysUntilExpiry > 90 && daysUntilExpiry <= 180;
                    
                case 'risk':
                    // High or Critical risk level
                    return riskLevel === 'high' || riskLevel === 'critical';
                    
                default:
                    return false;
            }
        });
        
        console.log(`[INFO] Found ${filteredContracts.length} contracts in ${category} category`);
        
        // Display filtered contracts
        displayFilteredWarnings(filteredContracts, category);
        
    } catch (error) {
        console.error('Error filtering warnings:', error);
    }
}

function displayFilteredWarnings(contracts, category) {
    const contractsContainer = document.getElementById('contracts-container');
    
    if (contracts.length === 0) {
        contractsContainer.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 20px;">ℹ️</div>
                <h3 style="color: #666; margin-bottom: 15px;">No contracts in this category</h3>
                <button onclick="loadContracts('warnings')" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 1rem; font-weight: 600;">
                    ← Back to All Warnings
                </button>
            </div>
        `;
        return;
    }
    
    // Get category details
    const categoryInfo = {
        critical: { icon: '🔴', name: 'Critical', description: 'Expiring ≤ 30 days or Expired', color: '#e74c3c' },
        warning: { icon: '🟡', name: 'Warning', description: 'Expiring 31-90 days', color: '#f39c12' },
        info: { icon: '🔵', name: 'Info', description: 'Expiring 91-180 days', color: '#3498db' },
        risk: { icon: '⚠️', name: 'High/Critical Risk', description: 'Contracts with elevated risk', color: '#e67e22' }
    };
    
    const cat = categoryInfo[category];
    const today = new Date();
    
    // Create header
    let headerHTML = `
        <div style="background: linear-gradient(135deg, ${cat.color} 0%, ${cat.color}dd 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                <h3 style="display: flex; align-items: center; gap: 10px; margin: 0;">
                    <span style="font-size: 2rem;">${cat.icon}</span>
                    <span>${cat.name} Contracts (${contracts.length})</span>
                </h3>
                <button onclick="loadContracts('warnings')" style="background: rgba(255,255,255,0.3); color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 0.9rem; font-weight: 600; transition: all 0.3s;" onmouseover="this.style.background='rgba(255,255,255,0.5)'" onmouseout="this.style.background='rgba(255,255,255,0.3)'">
                    ← Back to All Warnings
                </button>
            </div>
            <p style="margin: 0; opacity: 0.95;">${cat.description}</p>
        </div>
    `;
    
    // Create contract cards
    const cardsHTML = contracts.map(contract => {
        const startDate = new Date(contract.start_date).toLocaleDateString();
        const endDate = new Date(contract.end_date).toLocaleDateString();
        const value = contract.contract_value 
            ? new Intl.NumberFormat('en-US', { style: 'currency', currency: contract.currency }).format(contract.contract_value)
            : 'N/A';
        
        const summaryId = `summary-${contract.id}`;
        const hasFullSummary = contract.summary && contract.summary.length > 200;
        
        // Calculate warning badge
        const endDateObj = new Date(contract.end_date);
        const daysUntilExpiry = Math.ceil((endDateObj - today) / (1000 * 60 * 60 * 24));
        const riskLevel = contract.risk_level ? contract.risk_level.toLowerCase() : '';
        
        let warningType = '';
        let warningIcon = cat.icon;
        let warningColor = cat.color;
        
        if (category === 'critical' && daysUntilExpiry < 0) {
            warningType = 'Expired ' + Math.abs(daysUntilExpiry) + ' days ago';
        } else if (category === 'critical') {
            warningType = 'Expires in ' + daysUntilExpiry + ' days';
        } else if (category === 'warning') {
            warningType = 'Expires in ' + daysUntilExpiry + ' days';
        } else if (category === 'info') {
            warningType = 'Expires in ' + daysUntilExpiry + ' days';
        } else if (category === 'risk') {
            warningType = riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1) + ' Risk Level';
        }
        
        const warningBadge = `
            <div style="background: ${warningColor}; color: white; padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; margin-bottom: 10px; display: inline-block;">
                ${warningIcon} ${warningType}
            </div>
        `;
        
        return `
            <div class="contract-card" data-contract-id="${contract.id}">
                ${warningBadge}
                <div class="contract-header">
                    <div>
                        <div class="contract-title">${contract.contract_name}</div>
                        <div class="contract-number">Contract #${contract.contract_number}</div>
                    </div>
                    <div class="contract-status ${contract.status}">${contract.status}</div>
                </div>
                
                <div class="contract-details">
                    <div class="detail-item">
                        <span class="detail-label">Party A:</span> ${contract.party_a || 'N/A'}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Party B:</span> ${contract.party_b || 'N/A'}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Start Date:</span> ${startDate}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">End Date:</span> ${endDate}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Value:</span> ${value}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Risk Level:</span> 
                        <div style="display: inline-block;">
                            <span style="text-transform: uppercase; font-weight: bold; color: ${getRiskColor(contract.risk_level)}">${contract.risk_level}</span>
                            ${contract.risk_reason ? `<div style="font-size: 0.8rem; color: #666; font-style: italic; margin-top: 3px;">💡 ${contract.risk_reason}</div>` : ''}
                        </div>
                    </div>
                </div>
                
                ${contract.summary ? `
                    <div class="contract-summary-section">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <strong style="color: #1e3a5f; font-size: 1.1em;">🤖 AI-Generated Analysis</strong>
                            ${hasFullSummary ? `
                                <button class="btn-expand" onclick="toggleSummary('${summaryId}')" style="background: #2c5f7c; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 0.9em;">
                                    <span id="${summaryId}-btn-text">Show Full Analysis</span>
                                </button>
                            ` : ''}
                        </div>
                        <div id="${summaryId}" class="contract-summary-content" style="display: ${hasFullSummary ? 'none' : 'block'}; max-height: none; overflow: hidden; background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #2c5f7c;">
                            ${formatSummary(contract.summary)}
                        </div>
                        ${hasFullSummary ? `
                            <div id="${summaryId}-preview" class="contract-summary-preview" style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #2c5f7c; color: #555;">
                                ${contract.summary.substring(0, 200)}... <em style="color: #2c5f7c;">(Click "Show Full Analysis" to see complete details)</em>
                            </div>
                        ` : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    contractsContainer.innerHTML = headerHTML + cardsHTML;
}

// Make function globally available
window.filterWarningsByCategory = filterWarningsByCategory;

// ============================================================================
// SETUP STAT CARD CLICK HANDLERS
// ============================================================================
function setupStatCardClickHandlers() {
    // Total Contracts
    const totalCard = document.getElementById('stat-card-total');
    if (totalCard) {
        totalCard.addEventListener('click', () => {
            switchToContractsTab('all');
        });
    }
    
    // Active Contracts
    const activeCard = document.getElementById('stat-card-active');
    if (activeCard) {
        activeCard.addEventListener('click', () => {
            switchToContractsTab('active');
        });
    }
    
    // Expired Contracts
    const expiredCard = document.getElementById('stat-card-expired');
    if (expiredCard) {
        expiredCard.addEventListener('click', () => {
            switchToContractsTab('expired');
        });
    }
    
    // Renewed Contracts
    const renewedCard = document.getElementById('stat-card-renewed');
    if (renewedCard) {
        renewedCard.addEventListener('click', () => {
            switchToContractsTab('renewed');
        });
    }
    
    // Pending Contracts
    const pendingCard = document.getElementById('stat-card-pending');
    if (pendingCard) {
        pendingCard.addEventListener('click', () => {
            switchToContractsTab('pending');
        });
    }
    
    // Warning Contracts
    const warningCard = document.getElementById('stat-card-warning');
    if (warningCard) {
        warningCard.addEventListener('click', () => {
            switchToContractsTab('warning');
        });
    }
    
    // Risk Level Filters
    const riskLowCard = document.getElementById('stat-card-risk-low');
    if (riskLowCard) {
        riskLowCard.addEventListener('click', () => {
            switchToContractsTab('risk-low');
        });
    }
    
    const riskMediumCard = document.getElementById('stat-card-risk-medium');
    if (riskMediumCard) {
        riskMediumCard.addEventListener('click', () => {
            switchToContractsTab('risk-medium');
        });
    }
    
    const riskHighCard = document.getElementById('stat-card-risk-high');
    if (riskHighCard) {
        riskHighCard.addEventListener('click', () => {
            switchToContractsTab('risk-high');
        });
    }
    
    const riskCriticalCard = document.getElementById('stat-card-risk-critical');
    if (riskCriticalCard) {
        riskCriticalCard.addEventListener('click', () => {
            switchToContractsTab('risk-critical');
        });
    }
}

// Helper function to switch to contracts tab with filter
function switchToContractsTab(filterType) {
    // Switch to contracts tab
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    const contractsBtn = document.querySelector('[data-tab="contracts"]');
    contractsBtn.classList.add('active');
    document.getElementById('contracts-tab').classList.add('active');
    
    // Set filter and load contracts
    if (filterType === 'warning') {
        document.getElementById('status-filter').value = '';
        loadContracts('warnings');
    } else if (filterType === 'all') {
        document.getElementById('status-filter').value = '';
        loadContracts('all');
    } else if (filterType && filterType.startsWith('risk-')) {
        // Risk level filter - don't set status dropdown
        document.getElementById('status-filter').value = '';
        loadContracts(filterType);
    } else {
        document.getElementById('status-filter').value = filterType;
        loadContracts(filterType);
    }
}

// ============================================================================
// RE-ANALYZE CONTRACT
// ============================================================================
async function reanalyzeContract(contractId) {
    const button = event.target;
    const originalText = button.innerHTML;
    
    try {
        // Show loading state
        button.innerHTML = '⏳ Analyzing...';
        button.disabled = true;
        button.style.opacity = '0.6';
        button.style.cursor = 'not-allowed';
        
        // Call API to re-analyze
        const response = await fetch(`/api/contracts/${contractId}/reanalyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to re-analyze contract');
        }
        
        const result = await response.json();
        
        // Show success message
        alert(`✅ ${result.message}\n\n💡 Risk Reason: ${result.risk_reason}`);
        
        // Reload the contracts to show updated risk reason
        const currentFilter = document.getElementById('status-filter').value || 'all';
        loadContracts(currentFilter);
        
    } catch (error) {
        console.error('Error re-analyzing contract:', error);
        alert(`❌ Error: ${error.message}`);
        
        // Reset button
        button.innerHTML = originalText;
        button.disabled = false;
        button.style.opacity = '1';
        button.style.cursor = 'pointer';
    }
}

// ============================================================================
// BULK RE-ANALYZE ALL CONTRACTS
// ============================================================================
async function bulkReanalyzeContracts() {
    // Show confirmation dialog
    const confirmed = confirm(
        '🤖 AI Bulk Analysis\n\n' +
        'This will analyze ALL contracts that don\'t have risk reasons yet.\n\n' +
        '⏱️ This may take 3-5 minutes depending on the number of contracts.\n\n' +
        'The page will show a progress indicator. Do you want to continue?'
    );
    
    if (!confirmed) {
        return;
    }
    
    // Create progress overlay
    const overlay = document.createElement('div');
    overlay.id = 'progress-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    overlay.innerHTML = `
        <div style="background: white; padding: 40px; border-radius: 15px; text-align: center; max-width: 500px; box-shadow: 0 10px 50px rgba(0,0,0,0.5);">
            <div style="font-size: 4rem; margin-bottom: 20px;">🤖</div>
            <h2 style="color: #1e3a5f; margin-bottom: 15px;">AI Analyzing Contracts...</h2>
            <p style="color: #666; margin-bottom: 25px; font-size: 1.1rem;">Please wait while we analyze all contracts. This may take a few minutes.</p>
            <div style="background: #f0f0f0; height: 30px; border-radius: 15px; overflow: hidden; margin-bottom: 20px;">
                <div id="progress-bar" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; width: 0%; transition: width 0.3s; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.9rem;"></div>
            </div>
            <div id="progress-text" style="color: #555; font-size: 0.95rem;">Starting analysis...</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    try {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        // Simulate initial progress
        progressBar.style.width = '10%';
        progressBar.textContent = '10%';
        progressText.textContent = 'Connecting to AI...';
        
        // Call API
        const response = await fetch('/api/contracts/reanalyze-all', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to re-analyze contracts');
        }
        
        const result = await response.json();
        
        // Show completion
        progressBar.style.width = '100%';
        progressBar.textContent = '100%';
        progressText.textContent = 'Analysis complete!';
        
        // Wait a moment, then show results
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Remove overlay
        document.body.removeChild(overlay);
        
        // Show detailed results
        let resultMessage = `✅ Bulk Analysis Complete!\n\n`;
        resultMessage += `📊 Total Contracts: ${result.total}\n`;
        resultMessage += `✅ Successfully Analyzed: ${result.success}\n`;
        if (result.failed > 0) {
            resultMessage += `❌ Failed: ${result.failed}\n`;
        }
        resultMessage += `\n${result.message}`;
        
        alert(resultMessage);
        
        // Reload contracts to show updated risk reasons
        const currentFilter = document.getElementById('status-filter').value || 'all';
        loadContracts(currentFilter);
        
        // Reload dashboard stats
        loadDashboardStats();
        
    } catch (error) {
        console.error('Error during bulk re-analysis:', error);
        
        // Remove overlay
        if (document.getElementById('progress-overlay')) {
            document.body.removeChild(document.getElementById('progress-overlay'));
        }
        
        alert(`❌ Error: ${error.message}\n\nPlease try again or contact support if the issue persists.`);
    }
}

// ============================================================================
// INITIALIZE ON PAGE LOAD
// ============================================================================
// ============================================================================
// ACCORDION TOGGLE FOR ABOUT TAB
// ============================================================================
function toggleAccordion(header) {
    const accordionBody = header.nextElementSibling;
    const isActive = accordionBody.classList.contains('active');
    
    // Toggle active state
    header.classList.toggle('active');
    accordionBody.classList.toggle('active');
    
    // Update icon
    const icon = header.querySelector('.accordion-icon');
    icon.textContent = isActive ? '+' : '−';
}

// ============================================================================
// QUICK PROMPTS FOR ASK AI
// ============================================================================
function usePrompt(promptText) {
    // Get the question textarea
    const questionInput = document.getElementById('question');
    
    // Set the prompt text
    questionInput.value = promptText;
    
    // Focus on the textarea
    questionInput.focus();
    
    // Scroll to the input area
    questionInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Optional: Auto-submit the form after a short delay
    // Uncomment the following lines if you want auto-submit
    // setTimeout(() => {
    //     document.getElementById('ask-form').requestSubmit();
    // }, 500);
}

// ============================================================================
// TECHNICAL DOCUMENTATION - Moved to About Tab
// ============================================================================
// Technical documentation is now part of the About tab accordion system
// No modal functions needed

// ============================================================================
// DELETE CONTRACTS MODAL
// ============================================================================
async function openDeleteModal() {
    const modal = document.getElementById('deleteContractsModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Fetch all contracts
    try {
        const response = await fetch(`${API_BASE}/api/contracts?limit=1000`);
        const contracts = await response.json();
        
        // Sort contracts by number
        contracts.sort((a, b) => {
            const numA = a.contract_number || '';
            const numB = b.contract_number || '';
            return numA.localeCompare(numB);
        });
        
        // Populate list
        const listContainer = document.getElementById('contractDeleteList');
        
        if (contracts.length === 0) {
            listContainer.innerHTML = '<div class="no-contracts-message">No contracts available to delete.</div>';
            return;
        }
        
        listContainer.innerHTML = contracts.map(contract => {
            const riskClass = (contract.risk_level || 'low').toLowerCase();
            const statusBadge = getStatusBadge(contract.status || 'active');
            
            return `
                <div class="contract-delete-item">
                    <label>
                        <input type="checkbox" 
                               class="contract-checkbox" 
                               value="${contract.id}"
                               onchange="updateSelectedCount()">
                        <span class="contract-info">
                            <strong>${contract.contract_number || 'N/A'}</strong> - 
                            ${contract.contract_name || 'Untitled'} 
                            <span class="risk-badge risk-${riskClass}">${contract.risk_level || 'LOW'}</span>
                            ${statusBadge}
                        </span>
                    </label>
                </div>
            `;
        }).join('');
        
        updateSelectedCount();
    } catch (error) {
        console.error('Error loading contracts for deletion:', error);
        document.getElementById('contractDeleteList').innerHTML = 
            '<div class="error-message">Failed to load contracts. Please try again.</div>';
    }
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteContractsModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
    
    // Clear selections
    document.getElementById('selectAllContracts').checked = false;
    document.querySelectorAll('.contract-checkbox').forEach(cb => cb.checked = false);
    updateSelectedCount();
}

function toggleSelectAll() {
    const selectAll = document.getElementById('selectAllContracts');
    const checkboxes = document.querySelectorAll('.contract-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
    });
    
    updateSelectedCount();
}

function updateSelectedCount() {
    const checked = document.querySelectorAll('.contract-checkbox:checked');
    const count = checked.length;
    
    document.getElementById('selectedCount').textContent = count;
    document.getElementById('deleteCount').textContent = count;
    document.getElementById('deleteBtn').disabled = count === 0;
}

async function deleteSelectedContracts() {
    const checked = document.querySelectorAll('.contract-checkbox:checked');
    const contractIds = Array.from(checked).map(cb => parseInt(cb.value));
    
    if (contractIds.length === 0) {
        return;
    }
    
    // Confirmation with contract count
    const contractWord = contractIds.length === 1 ? 'contract' : 'contracts';
    const confirmed = confirm(
        `⚠️ Are you sure you want to delete ${contractIds.length} ${contractWord}?\n\nThis action cannot be undone.`
    );
    
    if (!confirmed) return;
    
    // Show progress
    const deleteBtn = document.getElementById('deleteBtn');
    const originalText = deleteBtn.innerHTML;
    deleteBtn.disabled = true;
    deleteBtn.innerHTML = '🔄 Deleting...';
    
    // Delete contracts one by one
    let deletedCount = 0;
    let failedCount = 0;
    
    for (const id of contractIds) {
        try {
            const response = await fetch(`${API_BASE}/api/contracts/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                deletedCount++;
                // Update progress
                deleteBtn.innerHTML = `🔄 Deleting... (${deletedCount}/${contractIds.length})`;
            } else {
                failedCount++;
                console.error(`Failed to delete contract ${id}: ${response.statusText}`);
            }
        } catch (error) {
            failedCount++;
            console.error(`Error deleting contract ${id}:`, error);
        }
    }
    
    // Show result
    if (failedCount === 0) {
        alert(`✅ Successfully deleted ${deletedCount} ${contractIds.length === 1 ? 'contract' : 'contracts'}!`);
    } else {
        alert(
            `Deletion completed:\n` +
            `✅ Deleted: ${deletedCount}\n` +
            `❌ Failed: ${failedCount}\n\n` +
            `Check console for details.`
        );
    }
    
    // Restore button
    deleteBtn.innerHTML = originalText;
    
    // Close modal and refresh
    closeDeleteModal();
    loadContracts();
    loadDashboardStats();
}

// Helper function to get status badge HTML
function getStatusBadge(status) {
    const statusClass = status.toLowerCase();
    return `<span class="status-badge status-${statusClass}">${status}</span>`;
}

// Close delete modal when clicking outside
document.getElementById('deleteContractsModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'deleteContractsModal') {
        closeDeleteModal();
    }
});

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    loadDashboardStats();
    loadContracts();
    loadContractsForSelect();  // Load contracts for the Ask AI dropdown on page load
    setupStatCardClickHandlers();
    
    // Setup delete contracts button
    const deleteBtn = document.getElementById('deleteContractsBtn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', openDeleteModal);
    }
    
    // Refresh critical count every 60 seconds
    setInterval(() => {
        loadDashboardStats();
    }, 60000);
});

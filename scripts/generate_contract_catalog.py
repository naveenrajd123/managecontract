"""
Generate Contract Catalog Templates
Creates multiple formats of contract descriptions for easy reference
"""

import json
import csv
from pathlib import Path
from datetime import datetime


def parse_contract_filename(filename):
    """Extract details from contract filename."""
    parts = filename.stem.split('_')
    if len(parts) < 4:
        return None
    
    return {
        'filename': filename.name,
        'contract_number': parts[0],
        'status': parts[1],
        'risk_level': parts[2],
        'contract_type': ' '.join(parts[3:]).replace('_', ' ')
    }


def read_contract_details(filepath):
    """Extract key details from contract content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract contract value
        import re
        value_match = re.search(r'Total Contract Value: \$([0-9,]+)', content)
        contract_value = value_match.group(1) if value_match else 'N/A'
        
        # Extract parties
        party_a_match = re.search(r'Party A.*?: ([^\n]+)', content)
        party_b_match = re.search(r'Party B.*?: ([^\n]+)', content)
        party_a = party_a_match.group(1).strip() if party_a_match else 'N/A'
        party_b = party_b_match.group(1).strip() if party_b_match else 'N/A'
        
        # Extract dates
        start_match = re.search(r'Start Date: ([^\n]+)', content)
        end_match = re.search(r'End Date: ([^\n]+)', content)
        start_date = start_match.group(1).strip() if start_match else 'N/A'
        end_date = end_match.group(1).strip() if end_match else 'N/A'
        
        # Extract compliance factors
        compliance_factors = []
        if 'HIPAA' in content:
            compliance_factors.append('HIPAA')
        if 'GDPR' in content:
            compliance_factors.append('GDPR')
        if 'PCI-DSS' in content:
            compliance_factors.append('PCI-DSS')
        if 'SOC 2' in content:
            compliance_factors.append('SOC 2')
        if 'FDA' in content:
            compliance_factors.append('FDA')
        if 'SOX' in content:
            compliance_factors.append('SOX')
        
        return {
            'contract_value': contract_value,
            'party_a': party_a,
            'party_b': party_b,
            'start_date': start_date,
            'end_date': end_date,
            'compliance': ', '.join(compliance_factors) if compliance_factors else 'Standard'
        }
    except Exception as e:
        return {
            'contract_value': 'N/A',
            'party_a': 'N/A',
            'party_b': 'N/A',
            'start_date': 'N/A',
            'end_date': 'N/A',
            'compliance': 'N/A'
        }


def generate_csv_catalog(contracts_data, output_file):
    """Generate CSV catalog."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Contract Number', 'Filename', 'Status', 'Risk Level', 'Contract Type',
            'Contract Value', 'Party A', 'Party B', 'Start Date', 'End Date', 'Compliance Factors'
        ])
        
        for contract in contracts_data:
            writer.writerow([
                contract['contract_number'],
                contract['filename'],
                contract['status'],
                contract['risk_level'],
                contract['contract_type'],
                contract['contract_value'],
                contract['party_a'],
                contract['party_b'],
                contract['start_date'],
                contract['end_date'],
                contract['compliance']
            ])
    
    print(f"[OK] Generated CSV catalog: {output_file}")


def generate_markdown_table(contracts_data, output_file):
    """Generate Markdown table format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Demo Contracts Catalog\n\n")
        f.write(f"**Total Contracts:** {len(contracts_data)}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n")
        
        # Summary by risk level
        risk_counts = {}
        status_counts = {}
        for contract in contracts_data:
            risk = contract['risk_level']
            status = contract['status']
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1
        
        f.write("## Summary\n\n")
        f.write("### Risk Levels\n")
        for risk in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            count = risk_counts.get(risk, 0)
            percentage = (count / len(contracts_data)) * 100
            emoji = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🟠', 'CRITICAL': '🔴'}[risk]
            f.write(f"- {emoji} **{risk}**: {count} contracts ({percentage:.1f}%)\n")
        
        f.write("\n### Statuses\n")
        for status in ['ACTIVE', 'EXPIRED', 'RENEWED', 'PENDING', 'WARNING']:
            count = status_counts.get(status, 0)
            percentage = (count / len(contracts_data)) * 100
            emoji = {'ACTIVE': '✅', 'EXPIRED': '⏰', 'RENEWED': '🔄', 'PENDING': '⏳', 'WARNING': '⚠️'}[status]
            f.write(f"- {emoji} **{status}**: {count} contracts ({percentage:.1f}%)\n")
        
        # Full table
        f.write("\n## Complete Contract List\n\n")
        f.write("| # | Contract | Type | Status | Risk | Value | Compliance |\n")
        f.write("|---|----------|------|--------|------|-------|------------|\n")
        
        for i, contract in enumerate(contracts_data, 1):
            risk_emoji = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🟠', 'CRITICAL': '🔴'}[contract['risk_level']]
            status_emoji = {'ACTIVE': '✅', 'EXPIRED': '⏰', 'RENEWED': '🔄', 'PENDING': '⏳', 'WARNING': '⚠️'}[contract['status']]
            
            f.write(f"| {i} | {contract['contract_number']} | {contract['contract_type']} | "
                   f"{status_emoji} {contract['status']} | {risk_emoji} {contract['risk_level']} | "
                   f"${contract['contract_value']} | {contract['compliance']} |\n")
        
        # Detailed sections
        f.write("\n## Contracts by Risk Level\n\n")
        for risk in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            matching = [c for c in contracts_data if c['risk_level'] == risk]
            if matching:
                emoji = {'LOW': '🟢', 'MEDIUM': '🟡', 'HIGH': '🟠', 'CRITICAL': '🔴'}[risk]
                f.write(f"\n### {emoji} {risk} Risk ({len(matching)} contracts)\n\n")
                for contract in matching:
                    f.write(f"- **{contract['contract_number']}**: {contract['contract_type']} "
                           f"({contract['status']}) - ${contract['contract_value']}\n")
    
    print(f"[OK] Generated Markdown catalog: {output_file}")


def generate_json_metadata(contracts_data, output_file):
    """Generate JSON metadata file."""
    metadata = {
        'generated': datetime.now().isoformat(),
        'total_contracts': len(contracts_data),
        'summary': {
            'risk_levels': {},
            'statuses': {}
        },
        'contracts': []
    }
    
    # Calculate summaries
    for contract in contracts_data:
        risk = contract['risk_level']
        status = contract['status']
        metadata['summary']['risk_levels'][risk] = metadata['summary']['risk_levels'].get(risk, 0) + 1
        metadata['summary']['statuses'][status] = metadata['summary']['statuses'].get(status, 0) + 1
    
    # Add contract details
    for contract in contracts_data:
        metadata['contracts'].append({
            'contract_number': contract['contract_number'],
            'filename': contract['filename'],
            'status': contract['status'],
            'risk_level': contract['risk_level'],
            'contract_type': contract['contract_type'],
            'financial': {
                'contract_value': contract['contract_value']
            },
            'parties': {
                'party_a': contract['party_a'],
                'party_b': contract['party_b']
            },
            'dates': {
                'start': contract['start_date'],
                'end': contract['end_date']
            },
            'compliance': contract['compliance'].split(', ') if contract['compliance'] != 'Standard' else []
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"[OK] Generated JSON metadata: {output_file}")


def generate_quick_reference(contracts_data, output_file):
    """Generate quick reference guide."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("DEMO CONTRACTS - QUICK REFERENCE GUIDE\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Total Contracts: {len(contracts_data)}\n")
        f.write(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n")
        
        # Test scenarios
        f.write("-"*80 + "\n")
        f.write("RECOMMENDED TEST SCENARIOS\n")
        f.write("-"*80 + "\n\n")
        
        f.write("1. LOW RISK CONTRACT (No major compliance)\n")
        low_contracts = [c for c in contracts_data if c['risk_level'] == 'LOW' and c['status'] == 'ACTIVE']
        if low_contracts:
            c = low_contracts[0]
            f.write(f"   File: {c['filename']}\n")
            f.write(f"   Value: ${c['contract_value']}\n")
            f.write(f"   Expected AI Assessment: LOW\n\n")
        
        f.write("2. MEDIUM RISK CONTRACT (Standard compliance)\n")
        medium_contracts = [c for c in contracts_data if c['risk_level'] == 'MEDIUM' and c['status'] == 'ACTIVE']
        if medium_contracts:
            c = medium_contracts[0]
            f.write(f"   File: {c['filename']}\n")
            f.write(f"   Value: ${c['contract_value']}\n")
            f.write(f"   Expected AI Assessment: MEDIUM\n\n")
        
        f.write("3. HIGH RISK CONTRACT (GDPR + PCI-DSS)\n")
        high_contracts = [c for c in contracts_data if c['risk_level'] == 'HIGH' and c['status'] == 'ACTIVE']
        if high_contracts:
            c = high_contracts[0]
            f.write(f"   File: {c['filename']}\n")
            f.write(f"   Value: ${c['contract_value']}\n")
            f.write(f"   Compliance: {c['compliance']}\n")
            f.write(f"   Expected AI Assessment: HIGH\n\n")
        
        f.write("4. CRITICAL RISK CONTRACT (HIPAA + FDA + SOX)\n")
        critical_contracts = [c for c in contracts_data if c['risk_level'] == 'CRITICAL' and c['status'] == 'ACTIVE']
        if critical_contracts:
            c = critical_contracts[0]
            f.write(f"   File: {c['filename']}\n")
            f.write(f"   Value: ${c['contract_value']}\n")
            f.write(f"   Compliance: {c['compliance']}\n")
            f.write(f"   Expected AI Assessment: CRITICAL\n\n")
        
        # Status examples
        f.write("-"*80 + "\n")
        f.write("CONTRACT STATUS EXAMPLES\n")
        f.write("-"*80 + "\n\n")
        
        for status in ['ACTIVE', 'EXPIRED', 'RENEWED', 'PENDING', 'WARNING']:
            contracts = [c for c in contracts_data if c['status'] == status][:3]
            f.write(f"\n{status} Contracts ({len([c for c in contracts_data if c['status'] == status])} total):\n")
            for c in contracts:
                f.write(f"  - {c['contract_number']}: {c['contract_type']} ({c['risk_level']})\n")
        
        # Compliance factors
        f.write("\n" + "-"*80 + "\n")
        f.write("COMPLIANCE FACTORS BY RISK LEVEL\n")
        f.write("-"*80 + "\n\n")
        
        f.write("LOW RISK:\n")
        f.write("  - Standard business regulations\n")
        f.write("  - No major compliance requirements\n\n")
        
        f.write("MEDIUM RISK:\n")
        f.write("  - Standard data protection practices\n")
        f.write("  - Industry best practices\n\n")
        
        f.write("HIGH RISK:\n")
        f.write("  - GDPR compliance required\n")
        f.write("  - PCI-DSS Level 1\n")
        f.write("  - SOC 2 Type II certification\n\n")
        
        f.write("CRITICAL RISK:\n")
        f.write("  - HIPAA/PHI handling\n")
        f.write("  - FDA regulations\n")
        f.write("  - SOX financial reporting\n")
        f.write("  - Export controls (ITAR/EAR)\n")
        f.write("  - Critical infrastructure protection\n\n")
        
        f.write("="*80 + "\n")
    
    print(f"[OK] Generated quick reference: {output_file}")


def generate_html_catalog(contracts_data, output_file):
    """Generate HTML catalog with search and filter."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo Contracts Catalog</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .summary-card {
            padding: 15px;
            border-radius: 8px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            font-size: 2rem;
        }
        .summary-card p {
            margin: 0;
            opacity: 0.9;
        }
        .filters {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #667eea;
            background: white;
            color: #667eea;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn:hover {
            background: #667eea;
            color: white;
        }
        .filter-btn.active {
            background: #667eea;
            color: white;
        }
        .search-box {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            text-align: left;
            position: sticky;
            top: 0;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .risk-low { background: #d1fae5; color: #065f46; }
        .risk-medium { background: #fef3c7; color: #92400e; }
        .risk-high { background: #fed7aa; color: #9a3412; }
        .risk-critical { background: #fee2e2; color: #991b1b; }
        .status-active { background: #d1fae5; color: #065f46; }
        .status-expired { background: #fee2e2; color: #991b1b; }
        .status-renewed { background: #dbeafe; color: #1e40af; }
        .status-pending { background: #fef3c7; color: #92400e; }
        .status-warning { background: #fed7aa; color: #9a3412; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📁 Demo Contracts Catalog</h1>
        <p>Total: <strong id="total-count">""" + str(len(contracts_data)) + """</strong> contracts</p>
        
        <div class="summary" id="summary"></div>
        
        <input type="text" class="search-box" id="search" placeholder="Search by contract number, type, or party...">
        
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="LOW">🟢 LOW</button>
            <button class="filter-btn" data-filter="MEDIUM">🟡 MEDIUM</button>
            <button class="filter-btn" data-filter="HIGH">🟠 HIGH</button>
            <button class="filter-btn" data-filter="CRITICAL">🔴 CRITICAL</button>
            <button class="filter-btn" data-filter="ACTIVE">✅ ACTIVE</button>
            <button class="filter-btn" data-filter="EXPIRED">⏰ EXPIRED</button>
            <button class="filter-btn" data-filter="RENEWED">🔄 RENEWED</button>
            <button class="filter-btn" data-filter="PENDING">⏳ PENDING</button>
            <button class="filter-btn" data-filter="WARNING">⚠️ WARNING</button>
        </div>
        
        <table id="contracts-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Contract</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Risk</th>
                    <th>Value</th>
                    <th>Compliance</th>
                </tr>
            </thead>
            <tbody id="contracts-body"></tbody>
        </table>
    </div>
    
    <script>
        const contracts = """ + json.dumps([{
            'number': c['contract_number'],
            'type': c['contract_type'],
            'status': c['status'],
            'risk': c['risk_level'],
            'value': c['contract_value'],
            'compliance': c['compliance'],
            'filename': c['filename']
        } for c in contracts_data]) + """;
        
        let currentFilter = 'all';
        let searchTerm = '';
        
        function renderContracts() {
            const tbody = document.getElementById('contracts-body');
            let filtered = contracts;
            
            if (currentFilter !== 'all') {
                filtered = contracts.filter(c => 
                    c.risk === currentFilter || c.status === currentFilter
                );
            }
            
            if (searchTerm) {
                const term = searchTerm.toLowerCase();
                filtered = filtered.filter(c =>
                    c.number.toLowerCase().includes(term) ||
                    c.type.toLowerCase().includes(term) ||
                    c.filename.toLowerCase().includes(term)
                );
            }
            
            tbody.innerHTML = filtered.map((c, i) => `
                <tr>
                    <td>${i + 1}</td>
                    <td><strong>${c.number}</strong><br><small>${c.filename}</small></td>
                    <td>${c.type}</td>
                    <td><span class="badge status-${c.status.toLowerCase()}">${c.status}</span></td>
                    <td><span class="badge risk-${c.risk.toLowerCase()}">${c.risk}</span></td>
                    <td>$${c.value}</td>
                    <td>${c.compliance}</td>
                </tr>
            `).join('');
            
            document.getElementById('total-count').textContent = filtered.length;
        }
        
        function renderSummary() {
            const risks = {};
            contracts.forEach(c => {
                risks[c.risk] = (risks[c.risk] || 0) + 1;
            });
            
            const summary = document.getElementById('summary');
            summary.innerHTML = Object.entries(risks).map(([risk, count]) => `
                <div class="summary-card">
                    <h3>${count}</h3>
                    <p>${risk} Risk</p>
                </div>
            `).join('');
        }
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderContracts();
            });
        });
        
        document.getElementById('search').addEventListener('input', (e) => {
            searchTerm = e.target.value;
            renderContracts();
        });
        
        renderSummary();
        renderContracts();
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] Generated HTML catalog: {output_file}")


def main():
    """Generate all catalog templates."""
    demo_dir = Path('demo_contracts')
    contracts = sorted([f for f in demo_dir.iterdir() if f.suffix == '.txt' and f.name != 'README.md'])
    
    print("="*60)
    print("Generating Contract Catalog Templates")
    print("="*60)
    print(f"\nProcessing {len(contracts)} contracts...\n")
    
    # Collect contract data
    contracts_data = []
    for contract_file in contracts:
        file_info = parse_contract_filename(contract_file)
        if file_info:
            details = read_contract_details(contract_file)
            contracts_data.append({**file_info, **details})
    
    # Generate all templates
    generate_csv_catalog(contracts_data, 'demo_contracts/CONTRACTS_CATALOG.csv')
    generate_markdown_table(contracts_data, 'demo_contracts/CONTRACTS_CATALOG.md')
    generate_json_metadata(contracts_data, 'demo_contracts/CONTRACTS_METADATA.json')
    generate_quick_reference(contracts_data, 'demo_contracts/QUICK_REFERENCE.txt')
    generate_html_catalog(contracts_data, 'demo_contracts/CONTRACTS_CATALOG.html')
    
    print("\n" + "="*60)
    print("All catalog templates generated!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. CONTRACTS_CATALOG.csv - Excel/spreadsheet format")
    print("  2. CONTRACTS_CATALOG.md - Markdown with tables")
    print("  3. CONTRACTS_METADATA.json - JSON for programmatic use")
    print("  4. QUICK_REFERENCE.txt - Quick reference guide")
    print("  5. CONTRACTS_CATALOG.html - Interactive HTML catalog")
    print("\nOpen CONTRACTS_CATALOG.html in your browser for best experience!")


if __name__ == "__main__":
    main()

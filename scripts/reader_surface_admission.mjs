import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const HASH = (value) => crypto.createHash('sha256').update(value).digest('hex');
const HANGUL = /[가-힣]/;
const ASCII_WORD = /[A-Za-z][A-Za-z0-9_-]*/g;

function normalize(text) {
  return String(text).replace(/\s+/g, ' ').trim();
}

function isVisibleSpecField(key, excluded) {
  return !excluded.includes(key);
}

function flattenText(value, path = '', rows = []) {
  if (typeof value === 'string') {
    const text = normalize(value);
    if (text) rows.push({path, text});
    return rows;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => flattenText(item, `${path}[${index}]`, rows));
    return rows;
  }
  if (value && typeof value === 'object') {
    Object.entries(value).forEach(([key, item]) => flattenText(item, `${path}.${key}`, rows));
  }
  return rows;
}

function writeReport(reportPath, report) {
  if (!reportPath) return;
  fs.mkdirSync(path.dirname(reportPath), {recursive: true});
  fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
}

export function createVisibleTextRegistry() {
  return [];
}

export function registerVisibleText(registry, text, objectName = '') {
  const normalized = normalize(text);
  if (!normalized) return;
  registry.push({object_name: objectName || 'unnamed_text', text: normalized});
}

function sourceGatewayFindings(sourceText, policy) {
  const findings = [];
  const gatewayPatterns = {
    'slide.addText': /\bslide\.addText\s*\(/g,
    'slide.addTable': /\bslide\.addTable\s*\(/g,
    'slide.addImage': /\bslide\.addImage\s*\(/g,
    'slide.addNotes': /\bslide\.addNotes\s*\(/g,
    'slide.addShape': /\bslide\.addShape\s*\(/g,
    'pptx.addSection': /\bpptx\.addSection\s*\(/g,
  };
  const counts = {};
  for (const [gateway, expected] of Object.entries(policy.source_policy.single_gateway_calls || {})) {
    const pattern = gatewayPatterns[gateway];
    if (!pattern) {
      findings.push({severity: 'error', code: 'unknown_gateway_policy', gateway, message: '정책이 알 수 없는 PPTX 진입점을 요구합니다.'});
      continue;
    }
    const actual = [...sourceText.matchAll(pattern)].length;
    counts[gateway] = actual;
    if (actual !== expected) {
      findings.push({severity: 'error', code: 'raw_gateway_bypass', gateway, expected, actual, message: `${gateway} 호출은 공용 게이트 ${expected}건이어야 하나 ${actual}건입니다.`});
    }
  }
  return {findings, counts};
}

function copyFindings(records, policy) {
  const findings = [];
  const allowedTerms = new Set([
    ...(policy.reader_copy_policy.allow_domain_terms || []),
    ...(policy.reader_copy_policy.allow_brand_terms || []),
    ...(policy.reader_copy_policy.allow_role_terms || []),
    ...(policy.reader_copy_policy.allow_interface_terms || []),
  ].map((term) => term.toLowerCase()));
  const forbiddenPatterns = policy.reader_copy_policy.forbidden_patterns.map((pattern) => new RegExp(pattern, 'i'));
  const forbiddenLiterals = policy.reader_copy_policy.forbidden_literals.map((literal) => literal.toLowerCase());

  for (const record of records) {
    for (const pattern of forbiddenPatterns) {
      if (pattern.test(record.text)) {
        findings.push({severity: 'error', code: 'internal_or_meta_copy', object_name: record.object_name, text: record.text, message: '독자 화면에 내부 제작·검증·작업 상태 언어가 들어갔습니다.'});
        break;
      }
    }
    if (forbiddenLiterals.some((literal) => record.text.toLowerCase().includes(literal))) {
      findings.push({severity: 'error', code: 'internal_literal_copy', object_name: record.object_name, text: record.text, message: '독자 화면에 내부 파일·식별 언어가 들어갔습니다.'});
    }
    const unknownEnglish = [...record.text.matchAll(ASCII_WORD)]
      .map((match) => match[0])
      .filter((term) => !allowedTerms.has(term.toLowerCase()));
    if (unknownEnglish.length) {
      findings.push({severity: 'error', code: 'unapproved_english_term', object_name: record.object_name, text: record.text, terms: [...new Set(unknownEnglish)], message: '독자 화면의 영어 용어는 강의 개념으로 명시 승인되어야 합니다.'});
    }
  }
  return findings;
}

function kickerFindings(specs, policy) {
  if (!policy.reader_copy_policy.require_hangul_kicker) return [];
  return specs
    .filter((spec) => !HANGUL.test(String(spec.kicker || '')))
    .map((spec) => ({severity: 'error', code: 'kicker_not_korean_reader_copy', slide_id: spec.id, text: spec.kicker || '', message: '상단 표지는 한국어 독자 문장으로 써야 합니다.'}));
}

function registryFindings(specs, records, policy) {
  if (!policy.source_policy.require_registered_visible_text) return [];
  const registered = records.map((record) => record.text);
  const findings = [];
  for (const spec of specs) {
    const publicPayload = {};
    for (const [key, value] of Object.entries(spec)) {
      if (isVisibleSpecField(key, policy.source_policy.exclude_spec_fields)) publicPayload[key] = value;
    }
    for (const row of flattenText(publicPayload, spec.id)) {
      if (!registered.some((visibleText) => visibleText === row.text || visibleText.includes(row.text))) {
        findings.push({severity: 'error', code: 'unregistered_spec_copy', slide_id: spec.id, path: row.path, text: row.text, message: '선언된 독자 문구가 공용 visible-text 게이트에서 확인되지 않았습니다.'});
      }
    }
  }
  return findings;
}

export function assertReaderSurfaceAdmission({specs, manifest, policy, visibleText, sourcePath, reportPath}) {
  const findings = [];
  if (specs.length !== manifest.slides.length || specs.some((spec, index) => spec.id !== manifest.slides[index].slide_id)) {
    findings.push({severity: 'error', code: 'manifest_payload_mismatch', message: '독자 문구 payload와 선언된 슬라이드 순서가 다릅니다.'});
  }
  const sourceText = fs.readFileSync(sourcePath, 'utf8');
  const gateway = sourceGatewayFindings(sourceText, policy);
  findings.push(...gateway.findings, ...kickerFindings(specs, policy), ...registryFindings(specs, visibleText, policy), ...copyFindings(visibleText, policy));
  const report = {
    schema_version: '1.0',
    status: findings.some((finding) => finding.severity === 'error') ? 'fail_local' : 'pass_local',
    artifact_id: policy.artifact_id,
    target_medium: policy.target_medium,
    surface: policy.surface,
    source_path: sourcePath,
    source_sha256: HASH(sourceText),
    policy_sha256: HASH(JSON.stringify(policy)),
    visible_text_count: visibleText.length,
    source_gateway: gateway.counts,
    findings,
    claim_boundary: policy.claim_boundary
  };
  writeReport(reportPath, report);
  if (report.status !== 'pass_local') {
    throw new Error(`Reader-surface admission failed. See ${reportPath}`);
  }
  return report;
}

#!/usr/bin/env node
/**
 * Mermaid Syntax Validator
 * Validates all .mmd files in the mermaid folder
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import mermaid from 'mermaid/dist/mermaid.esm.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const { parse } = mermaid;

async function validateFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    try {
        parse(content, { suppressErrors: false });
        return { valid: true, error: null };
    } catch (e) {
        return { valid: false, error: e.message };
    }
}

async function main() {
    const mermaidDir = path.join(__dirname, 'mermaid');
    const allFiles = [];

    function findMmdFiles(dir) {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.isDirectory()) {
                findMmdFiles(fullPath);
            } else if (entry.name.endsWith('.mmd')) {
                allFiles.push(fullPath);
            }
        }
    }

    findMmdFiles(mermaidDir);

    console.log(`\nFound ${allFiles.length} Mermaid files to validate\n`);
    console.log('='.repeat(60));

    let hasErrors = false;

    for (const file of allFiles) {
        const relPath = path.relative(__dirname, file);
        process.stdout.write(`\nChecking: ${relPath} ...`);

        const result = await validateFile(file);

        if (result.valid) {
            console.log(' ✓ OK');
        } else {
            console.log(' ✗ ERROR');
            console.log(`  Error: ${result.error}`);
            hasErrors = true;
        }
    }

    console.log('\n' + '='.repeat(60));

    if (hasErrors) {
        console.log('\n❌ Some files have syntax errors\n');
        process.exit(1);
    } else {
        console.log('\n✓ All files are valid\n');
        process.exit(0);
    }
}

main().catch(e => {
    console.error('Validation failed:', e);
    process.exit(1);
});
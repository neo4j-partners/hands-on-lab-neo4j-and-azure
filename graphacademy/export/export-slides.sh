#!/bin/bash
#
# export-slides.sh
# Exports Marp markdown slides to PDF format
#
# This script:
# 1. Finds all slide markdown files in graphacademy/slides subdirectories
# 2. Converts each to PDF using Marp CLI
# 3. Merges PDFs per lab directory
# 4. Optionally creates a combined all-labs PDF
#
# Requirements:
# - marp-cli (npm install -g @marp-team/marp-cli)
# - macOS (uses built-in PDF join utility)
#
# Usage:
#   ./export-slides.sh              # Export all labs
#   ./export-slides.sh --lab 1      # Export only lab-1
#   ./export-slides.sh --combined   # Also create combined PDF of all labs
#   ./export-slides.sh --clean      # Clean up all generated PDFs
#

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SLIDES_DIR="$PROJECT_ROOT/graphacademy/slides"
EXPORT_DIR="$SCRIPT_DIR"
TEMP_DIR="$EXPORT_DIR/.temp"

# macOS PDF join utility
PDF_JOIN="/System/Library/Automator/Combine PDF Pages.action/Contents/MacOS/join"

# =============================================================================
# Color Output
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()    { echo -e "${CYAN}[STEP]${NC} $1"; }

# =============================================================================
# Help
# =============================================================================

show_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Export Marp markdown slides to PDF format.

Options:
    -h, --help          Show this help message
    -l, --lab NUMBER    Export only the specified lab (e.g., --lab 1)
    -c, --combined      Create a combined PDF of all labs
    --clean             Remove all generated PDFs and temp files
    --keep-temp         Keep intermediate PDF files (for debugging)
    --scale FACTOR      Image scale factor for PDF (default: 2)

Examples:
    $(basename "$0")                    # Export all labs
    $(basename "$0") --lab 1            # Export only lab-1
    $(basename "$0") --combined         # Export all + combined PDF
    $(basename "$0") --clean            # Clean up all PDFs

EOF
}

# =============================================================================
# Dependency Checks
# =============================================================================

check_dependencies() {
    log_step "Checking dependencies..."

    local missing=0

    # Check for marp
    if ! command -v marp &> /dev/null; then
        log_error "marp-cli is not installed"
        log_info "Install with: npm install -g @marp-team/marp-cli"
        missing=1
    else
        log_success "marp-cli found: $(marp --version)"
    fi

    # Check for macOS PDF join utility
    if [[ ! -x "$PDF_JOIN" ]]; then
        log_error "macOS PDF join utility not found at: $PDF_JOIN"
        log_info "This script requires macOS"
        missing=1
    else
        log_success "macOS PDF join utility found"
    fi

    if [[ $missing -eq 1 ]]; then
        exit 1
    fi
}

# =============================================================================
# Cleanup Functions
# =============================================================================

cleanup_temp() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
        log_info "Cleaned up temp directory"
    fi
}

cleanup_all() {
    log_step "Cleaning up all generated files..."

    # Remove temp directory
    cleanup_temp

    # Remove generated PDFs
    find "$EXPORT_DIR" -name "*.pdf" -type f -delete 2>/dev/null || true

    log_success "All generated files removed"
}

# =============================================================================
# Export Functions
# =============================================================================

# Convert a single markdown file to PDF
convert_to_pdf() {
    local input_file="$1"
    local output_file="$2"
    local scale="${3:-2}"

    log_info "Converting: $(basename "$input_file")"

    # Run marp with allow-local-files for image access
    if ! marp --pdf \
              --allow-local-files \
              --pdf-notes \
              --image-scale "$scale" \
              "$input_file" \
              -o "$output_file" 2>&1; then
        log_error "Failed to convert: $input_file"
        return 1
    fi

    return 0
}

# Merge multiple PDFs into one
merge_pdfs() {
    local output_file="$1"
    shift
    local -a input_files=("$@")

    if [[ ${#input_files[@]} -eq 0 ]]; then
        log_warn "No PDFs to merge"
        return 1
    fi

    if [[ ${#input_files[@]} -eq 1 ]]; then
        # Only one file, just copy it
        cp "${input_files[0]}" "$output_file"
        return 0
    fi

    log_info "Merging ${#input_files[@]} PDFs into: $(basename "$output_file")"

    if ! "$PDF_JOIN" -o "$output_file" "${input_files[@]}" 2>&1; then
        log_error "Failed to merge PDFs"
        return 1
    fi

    return 0
}

# Export a single lab
export_lab() {
    local lab_dir="$1"
    local lab_name
    lab_name="$(basename "$lab_dir")"
    local scale="$2"
    local keep_temp="$3"

    log_step "Exporting: $lab_name"

    # Create temp directory for this lab
    local lab_temp_dir="$TEMP_DIR/$lab_name"
    mkdir -p "$lab_temp_dir"

    # Get all slide files (bash 3.2 compatible)
    local -a slide_files=()
    while IFS= read -r file; do
        [[ -n "$file" ]] && slide_files+=("$file")
    done < <(find "$lab_dir" -maxdepth 1 -name "*-slides.md" -type f | sort)

    if [[ ${#slide_files[@]} -eq 0 ]]; then
        log_warn "No slide files found in: $lab_name"
        return 0
    fi

    log_info "Found ${#slide_files[@]} slide file(s) in $lab_name"

    # Convert each slide file to PDF
    local -a pdf_files=()
    local failed=0

    for slide_file in "${slide_files[@]}"; do
        local base
        base="$(basename "$slide_file" .md)"
        local pdf_file="$lab_temp_dir/${base}.pdf"

        if convert_to_pdf "$slide_file" "$pdf_file" "$scale"; then
            pdf_files+=("$pdf_file")
        else
            failed=$((failed + 1))
        fi
    done

    if [[ $failed -gt 0 ]]; then
        log_warn "$failed file(s) failed to convert in $lab_name"
    fi

    # Merge PDFs for this lab
    if [[ ${#pdf_files[@]} -gt 0 ]]; then
        local output_pdf="$EXPORT_DIR/${lab_name}.pdf"
        if merge_pdfs "$output_pdf" "${pdf_files[@]}"; then
            log_success "Created: ${lab_name}.pdf"
        fi
    fi

    # Clean up temp files unless --keep-temp
    if [[ "$keep_temp" != "true" ]]; then
        rm -rf "$lab_temp_dir"
    fi

    return 0
}

# Export all labs
export_all_labs() {
    local scale="$1"
    local keep_temp="$2"
    local create_combined="$3"

    log_step "Finding lab directories..."

    # Find all lab directories (bash 3.2 compatible)
    local -a lab_dirs=()
    while IFS= read -r dir; do
        [[ -n "$dir" ]] && lab_dirs+=("$dir")
    done < <(find "$SLIDES_DIR" -maxdepth 1 -type d -name "lab-*" | sort)

    if [[ ${#lab_dirs[@]} -eq 0 ]]; then
        log_error "No lab directories found in: $SLIDES_DIR"
        exit 1
    fi

    log_info "Found ${#lab_dirs[@]} lab directories"

    # Create temp directory
    mkdir -p "$TEMP_DIR"

    # Export each lab
    for lab_dir in "${lab_dirs[@]}"; do
        export_lab "$lab_dir" "$scale" "$keep_temp"
        echo ""
    done

    # Create combined PDF if requested
    if [[ "$create_combined" == "true" ]]; then
        log_step "Creating combined PDF..."

        local -a lab_pdfs=()
        while IFS= read -r pdf; do
            [[ -n "$pdf" ]] && lab_pdfs+=("$pdf")
        done < <(find "$EXPORT_DIR" -maxdepth 1 -name "lab-*.pdf" -type f | sort)

        if [[ ${#lab_pdfs[@]} -gt 0 ]]; then
            local combined_pdf="$EXPORT_DIR/all-labs-combined.pdf"
            if merge_pdfs "$combined_pdf" "${lab_pdfs[@]}"; then
                log_success "Created: all-labs-combined.pdf"
            fi
        fi
    fi

    # Final cleanup
    if [[ "$keep_temp" != "true" ]]; then
        cleanup_temp
    fi
}

# Export a specific lab by number
export_single_lab() {
    local lab_num="$1"
    local scale="$2"
    local keep_temp="$3"

    # Find the lab directory
    local lab_dir
    lab_dir=$(find "$SLIDES_DIR" -maxdepth 1 -type d -name "lab-${lab_num}-*" | head -1)

    if [[ -z "$lab_dir" ]]; then
        log_error "Lab $lab_num not found in: $SLIDES_DIR"
        log_info "Available labs:"
        find "$SLIDES_DIR" -maxdepth 1 -type d -name "lab-*" -exec basename {} \; | sort
        exit 1
    fi

    # Create temp directory
    mkdir -p "$TEMP_DIR"

    export_lab "$lab_dir" "$scale" "$keep_temp"

    # Cleanup
    if [[ "$keep_temp" != "true" ]]; then
        cleanup_temp
    fi
}

# =============================================================================
# Main
# =============================================================================

main() {
    local lab_number=""
    local create_combined="false"
    local do_clean="false"
    local keep_temp="false"
    local scale="2"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                show_help
                exit 0
                ;;
            -l|--lab)
                lab_number="$2"
                shift 2
                ;;
            -c|--combined)
                create_combined="true"
                shift
                ;;
            --clean)
                do_clean="true"
                shift
                ;;
            --keep-temp)
                keep_temp="true"
                shift
                ;;
            --scale)
                scale="$2"
                shift 2
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║       Marp Slides PDF Exporter         ║"
    echo "╚════════════════════════════════════════╝"
    echo ""

    # Handle clean
    if [[ "$do_clean" == "true" ]]; then
        cleanup_all
        exit 0
    fi

    # Check dependencies
    check_dependencies
    echo ""

    # Export
    if [[ -n "$lab_number" ]]; then
        export_single_lab "$lab_number" "$scale" "$keep_temp"
    else
        export_all_labs "$scale" "$keep_temp" "$create_combined"
    fi

    echo ""
    log_success "Export complete!"
    echo ""
    log_info "Output directory: $EXPORT_DIR"
    ls -lh "$EXPORT_DIR"/*.pdf 2>/dev/null || true
}

main "$@"

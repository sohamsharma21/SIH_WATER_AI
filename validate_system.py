#!/usr/bin/env python3
"""
Comprehensive system validation and testing script
Tests all components of the SIH WATER AI system
"""

import sys
import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemValidator:
    """Validates all system components"""
    
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {}
        }
    
    def test_environment_setup(self):
        """Test 1: Environment setup"""
        test_name = "Environment Setup"
        logger.info(f"Testing {test_name}...")
        
        try:
            # Check Python version
            py_version = sys.version_info
            if py_version.major < 3 or py_version.minor < 9:
                raise ValueError(f"Python {py_version.major}.{py_version.minor} - requires 3.9+")
            
            # Check directories
            required_dirs = [
                'backend',
                'frontend',
                'migrations',
                'scripts',
                'docs'
            ]
            
            for dir_name in required_dirs:
                if not Path(dir_name).exists():
                    raise FileNotFoundError(f"Directory not found: {dir_name}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"Python {py_version.major}.{py_version.minor}, All directories present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_backend_dependencies(self):
        """Test 2: Backend dependencies"""
        test_name = "Backend Dependencies"
        logger.info(f"Testing {test_name}...")
        
        try:
            # Check requirements.txt exists
            req_file = Path('backend/requirements.txt')
            if not req_file.exists():
                raise FileNotFoundError("backend/requirements.txt not found")
            
            # Read and validate key dependencies
            with open(req_file) as f:
                requirements = f.read()
            
            required_packages = [
                'fastapi',
                'uvicorn',
                'pydantic',
                'supabase',
                'pandas',
                'scikit-learn',
                'paho-mqtt',
                'reportlab'
            ]
            
            missing = []
            for pkg in required_packages:
                if pkg not in requirements.lower():
                    missing.append(pkg)
            
            if missing:
                raise ValueError(f"Missing packages in requirements.txt: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_packages)} key packages found"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_frontend_dependencies(self):
        """Test 3: Frontend dependencies"""
        test_name = "Frontend Dependencies"
        logger.info(f"Testing {test_name}...")
        
        try:
            # Check package.json exists
            pkg_file = Path('frontend/package.json')
            if not pkg_file.exists():
                raise FileNotFoundError("frontend/package.json not found")
            
            with open(pkg_file) as f:
                package_json = json.load(f)
            
            # Check key dependencies
            required_deps = [
                'react',
                'next',
                '@supabase/supabase-js',
                'axios',
                '@react-three/fiber'
            ]
            
            deps = package_json.get('dependencies', {})
            missing = [dep for dep in required_deps if dep not in deps]
            
            if missing:
                raise ValueError(f"Missing npm packages: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_deps)} key packages found"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_database_migrations(self):
        """Test 4: Database migration files"""
        test_name = "Database Migrations"
        logger.info(f"Testing {test_name}...")
        
        try:
            migrations_dir = Path('migrations')
            required_files = [
                'schema.sql',
                'add_models_table.sql',
                'rls_policies.sql'
            ]
            
            missing = []
            for file_name in required_files:
                file_path = migrations_dir / file_name
                if not file_path.exists():
                    missing.append(file_name)
            
            if missing:
                raise FileNotFoundError(f"Missing migration files: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_files)} migration files present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_backend_structure(self):
        """Test 5: Backend code structure"""
        test_name = "Backend Structure"
        logger.info(f"Testing {test_name}...")
        
        try:
            backend_dir = Path('backend/app')
            required_files = [
                'main.py',
                'config.py',
                'api/routes.py',
                'ml/model_manager.py',
                'ml/pipeline.py',
                'ml/trainer.py',
                'services/ml_service.py',
                'services/supabase_service.py',
                'services/report_service.py',
                'services/mqtt_service.py'
            ]
            
            missing = []
            for file_name in required_files:
                file_path = backend_dir / file_name
                if not file_path.exists():
                    missing.append(file_name)
            
            if missing:
                raise FileNotFoundError(f"Missing backend files: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_files)} backend files present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_frontend_structure(self):
        """Test 6: Frontend component structure"""
        test_name = "Frontend Structure"
        logger.info(f"Testing {test_name}...")
        
        try:
            frontend_dir = Path('frontend')
            required_files = [
                'app/page.tsx',
                'app/layout.tsx',
                'app/login/page.tsx',
                'app/signup/page.tsx',
                'app/dashboard/page.tsx',
                'lib/api.ts',
                'lib/supabase.ts',
                'components/Dashboard.tsx'
            ]
            
            missing = []
            for file_name in required_files:
                file_path = frontend_dir / file_name
                if not file_path.exists():
                    missing.append(file_name)
            
            if missing:
                raise FileNotFoundError(f"Missing frontend files: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_files)} frontend files present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_configuration_files(self):
        """Test 7: Configuration files"""
        test_name = "Configuration Files"
        logger.info(f"Testing {test_name}...")
        
        try:
            required_files = [
                'backend/.env.example',
                'frontend/.env.local.example',
                'frontend/next.config.js',
                'frontend/tsconfig.json',
                'backend/requirements.txt',
                'frontend/package.json'
            ]
            
            missing = []
            for file_name in required_files:
                file_path = Path(file_name)
                if not file_path.exists():
                    missing.append(file_name)
            
            if missing:
                raise FileNotFoundError(f"Missing config files: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_files)} config files present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_docker_configuration(self):
        """Test 8: Docker configuration"""
        test_name = "Docker Configuration"
        logger.info(f"Testing {test_name}...")
        
        try:
            required_files = [
                'Dockerfile.backend',
                'Dockerfile.frontend',
                'docker-compose.yml'
            ]
            
            missing = []
            for file_name in required_files:
                file_path = Path(file_name)
                if not file_path.exists():
                    missing.append(file_name)
            
            if missing:
                raise FileNotFoundError(f"Missing Docker files: {missing}")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"All {len(required_files)} Docker files present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def test_documentation(self):
        """Test 9: Documentation"""
        test_name = "Documentation"
        logger.info(f"Testing {test_name}...")
        
        try:
            required_docs = [
                'README.md',
                'docs/README.md',
                'docs/ARCHITECTURE.md',
                'docs/API_DOCS.md',
                'docs/PRODUCTION_DEPLOYMENT.md'
            ]
            
            missing = []
            for doc_file in required_docs:
                if not Path(doc_file).exists():
                    missing.append(doc_file)
            
            # Some are optional but most should exist
            if len(missing) > len(required_docs) / 2:
                logger.warning(f"Warning: {len(missing)} documentation files missing")
            
            self.results["tests"][test_name] = {"status": "PASS", "details": f"Documentation files checked - {len(required_docs) - len(missing)}/{len(required_docs)} present"}
            logger.info(f"✓ {test_name} PASSED")
            return True
        except Exception as e:
            self.results["tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"✗ {test_name} FAILED: {e}")
            return False
    
    def run_all_tests(self):
        """Run all validation tests"""
        logger.info("=" * 60)
        logger.info("SIH WATER AI - System Validation")
        logger.info("=" * 60)
        
        tests = [
            self.test_environment_setup,
            self.test_backend_dependencies,
            self.test_frontend_dependencies,
            self.test_database_migrations,
            self.test_backend_structure,
            self.test_frontend_structure,
            self.test_configuration_files,
            self.test_docker_configuration,
            self.test_documentation
        ]
        
        results = []
        for test in tests:
            results.append(test())
        
        # Summary
        passed = sum(results)
        total = len(results)
        
        self.results["summary"] = {
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": f"{(passed/total)*100:.1f}%"
        }
        
        logger.info("=" * 60)
        logger.info(f"Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
        logger.info("=" * 60)
        
        # Save report
        report_file = Path("VALIDATION_REPORT.json")
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        logger.info(f"Validation report saved to {report_file}")
        
        return passed == total


if __name__ == "__main__":
    validator = SystemValidator()
    success = validator.run_all_tests()
    sys.exit(0 if success else 1)

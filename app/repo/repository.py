"""
Repository layer for database operations
"""
import sqlite3
from typing import List, Optional, Tuple

from app.core.database import db_manager
from app.core.logger import logger, log_database_operation, log_error


class BankRepository:
    """Repository for Bank database operations"""
    
    def __init__(self):
        self.db = db_manager
        logger.info("BankRepository initialized")
    
    def get_all_banks(self, limit: int = 100, offset: int = 0) -> List[sqlite3.Row]:
        """
        Get all banks with pagination
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
        
        Returns:
            List of bank records
        """
        query = """
            SELECT id, name 
            FROM banks 
            ORDER BY name
            LIMIT ? OFFSET ?
        """
        logger.info(f"Fetching banks - limit: {limit}, offset: {offset}")
        try:
            results = self.db.execute_query(query, (limit, offset))
            log_database_operation("get_all_banks", f"Retrieved {len(results)} banks")
            return results
        except Exception as e:
            log_error(e, "Error fetching banks")
            raise
    
    def get_bank_by_id(self, bank_id: int) -> Optional[sqlite3.Row]:
        """
        Get bank by ID
        
        Args:
            bank_id: Bank ID
        
        Returns:
            Bank record or None
        """
        query = "SELECT id, name FROM banks WHERE id = ?"
        logger.info(f"Fetching bank by ID: {bank_id}")
        try:
            result = self.db.execute_one(query, (bank_id,))
            log_database_operation("get_bank_by_id", f"Bank ID: {bank_id}")
            return result
        except Exception as e:
            log_error(e, f"Error fetching bank ID: {bank_id}")
            raise
    
    def get_bank_by_name(self, name: str) -> Optional[sqlite3.Row]:
        """
        Get bank by name
        
        Args:
            name: Bank name
        
        Returns:
            Bank record or None
        """
        query = "SELECT id, name FROM banks WHERE name = ?"
        logger.info(f"Fetching bank by name: {name}")
        try:
            result = self.db.execute_one(query, (name,))
            log_database_operation("get_bank_by_name", f"Bank: {name}")
            return result
        except Exception as e:
            log_error(e, f"Error fetching bank: {name}")
            raise
    
    def search_banks(self, name_pattern: str, limit: int = 100) -> List[sqlite3.Row]:
        """
        Search banks by name pattern
        
        Args:
            name_pattern: Pattern to search (SQL LIKE pattern)
            limit: Maximum number of results
        
        Returns:
            List of matching bank records
        """
        query = """
            SELECT id, name 
            FROM banks 
            WHERE name LIKE ?
            ORDER BY name
            LIMIT ?
        """
        logger.info(f"Searching banks with pattern: {name_pattern}")
        try:
            results = self.db.execute_query(query, (f"%{name_pattern}%", limit))
            log_database_operation("search_banks", f"Found {len(results)} banks")
            return results
        except Exception as e:
            log_error(e, f"Error searching banks: {name_pattern}")
            raise
    
    def count_banks(self) -> int:
        """
        Count total number of banks
        
        Returns:
            Total count of banks
        """
        query = "SELECT COUNT(*) as count FROM banks"
        logger.debug("Counting total banks")
        try:
            result = self.db.execute_one(query)
            count = result['count'] if result else 0
            log_database_operation("count_banks", f"Total: {count}")
            return count
        except Exception as e:
            log_error(e, "Error counting banks")
            raise


class BranchRepository:
    """Repository for Branch database operations"""
    
    def __init__(self):
        self.db = db_manager
        logger.info("BranchRepository initialized")
    
    def get_all_branches(self, limit: int = 100, offset: int = 0) -> List[sqlite3.Row]:
        """
        Get all branches with bank information
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
        
        Returns:
            List of branch records with bank data
        """
        query = """
            SELECT 
                b.ifsc, b.branch, b.address, b.city, b.district, b.state,
                b.bank_id, ba.name as bank_name
            FROM branches b
            JOIN banks ba ON b.bank_id = ba.id
            ORDER BY b.ifsc
            LIMIT ? OFFSET ?
        """
        logger.info(f"Fetching branches - limit: {limit}, offset: {offset}")
        try:
            results = self.db.execute_query(query, (limit, offset))
            log_database_operation("get_all_branches", f"Retrieved {len(results)} branches")
            return results
        except Exception as e:
            log_error(e, "Error fetching branches")
            raise
    
    def get_branch_by_ifsc(self, ifsc: str) -> Optional[sqlite3.Row]:
        """
        Get branch by IFSC code
        
        Args:
            ifsc: IFSC code
        
        Returns:
            Branch record with bank data or None
        """
        query = """
            SELECT 
                b.ifsc, b.branch, b.address, b.city, b.district, b.state,
                b.bank_id, ba.name as bank_name
            FROM branches b
            JOIN banks ba ON b.bank_id = ba.id
            WHERE b.ifsc = ?
        """
        logger.info(f"Fetching branch by IFSC: {ifsc}")
        try:
            result = self.db.execute_one(query, (ifsc,))
            log_database_operation("get_branch_by_ifsc", f"IFSC: {ifsc}")
            return result
        except Exception as e:
            log_error(e, f"Error fetching branch IFSC: {ifsc}")
            raise
    
    def search_branches(
        self,
        ifsc: Optional[str] = None,
        city: Optional[str] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        bank_name: Optional[str] = None,
        branch_name: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[sqlite3.Row], int]:
        """
        Search branches with filters
        
        Args:
            ifsc: IFSC code pattern
            city: City name pattern
            district: District name pattern
            state: State name pattern
            bank_name: Bank name pattern
            branch_name: Branch name pattern
            limit: Maximum number of results
            offset: Number of records to skip
        
        Returns:
            Tuple of (list of matching branches, total count)
        """
        conditions = []
        params = []
        
        if ifsc:
            conditions.append("b.ifsc LIKE ?")
            params.append(f"%{ifsc}%")
        
        if city:
            conditions.append("b.city LIKE ?")
            params.append(f"%{city}%")
        
        if district:
            conditions.append("b.district LIKE ?")
            params.append(f"%{district}%")
        
        if state:
            conditions.append("b.state LIKE ?")
            params.append(f"%{state}%")
        
        if bank_name:
            conditions.append("ba.name LIKE ?")
            params.append(f"%{bank_name}%")
        
        if branch_name:
            conditions.append("b.branch LIKE ?")
            params.append(f"%{branch_name}%")
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # Count query
        count_query = f"""
            SELECT COUNT(*) as count
            FROM branches b
            JOIN banks ba ON b.bank_id = ba.id
            WHERE {where_clause}
        """
        
        # Data query
        data_query = f"""
            SELECT 
                b.ifsc, b.branch, b.address, b.city, b.district, b.state,
                b.bank_id, ba.name as bank_name
            FROM branches b
            JOIN banks ba ON b.bank_id = ba.id
            WHERE {where_clause}
            ORDER BY b.ifsc
            LIMIT ? OFFSET ?
        """
        
        logger.info(f"Searching branches with filters - limit: {limit}, offset: {offset}")
        try:
            # Get total count
            count_result = self.db.execute_one(count_query, tuple(params))
            total_count = count_result['count'] if count_result else 0
            
            # Get data
            data_params = params + [limit, offset]
            results = self.db.execute_query(data_query, tuple(data_params))
            
            log_database_operation(
                "search_branches",
                f"Found {len(results)} of {total_count} total branches"
            )
            return results, total_count
        except Exception as e:
            log_error(e, "Error searching branches")
            raise
    
    def count_branches(self) -> int:
        """
        Count total number of branches
        
        Returns:
            Total count of branches
        """
        query = "SELECT COUNT(*) as count FROM branches"
        logger.debug("Counting total branches")
        try:
            result = self.db.execute_one(query)
            count = result['count'] if result else 0
            log_database_operation("count_branches", f"Total: {count}")
            return count
        except Exception as e:
            log_error(e, "Error counting branches")
            raise


# Global repository instances
bank_repo = BankRepository()
branch_repo = BranchRepository()


def get_bank_repo() -> BankRepository:
    """Get bank repository instance"""
    return bank_repo


def get_branch_repo() -> BranchRepository:
    """Get branch repository instance"""
    return branch_repo

"""
Service layer - Business logic for Bank Branches API
"""
import base64
from typing import Optional, List

from app.core.logger import logger, log_error
from app.core.config import settings
from app.repo import get_branch_repo, get_bank_repo
from app.schemas import (
    BankType,
    BranchType,
    BranchEdge,
    BankEdge,
    BranchConnection,
    BankConnection,
    PageInfo,
    BranchFilterInput,
)


class BankService:
    """Service for bank-related business logic"""
    
    def __init__(self):
        self.repo = get_bank_repo()
        logger.info("BankService initialized")
    
    def get_all_banks(
        self,
        first: int = 20,
        after: Optional[str] = None
    ) -> BankConnection:
        """
        Get all banks with pagination
        
        Args:
            first: Number of records to return
            after: Cursor for pagination
        
        Returns:
            BankConnection with edges and page info
        """
        logger.info(f"Getting banks - first: {first}, after: {after}")
        
        try:
            # Decode cursor to get offset
            offset = 0
            if after:
                try:
                    offset = int(base64.b64decode(after).decode()) + 1
                except Exception as e:
                    log_error(e, "Invalid cursor")
                    offset = 0
            
            # Apply max page size limit
            limit = min(first, settings.MAX_PAGE_SIZE)
            
            # Get data from repository
            bank_rows = self.repo.get_all_banks(limit=limit + 1, offset=offset)
            total_count = self.repo.count_banks()
            
            # Check if there are more results
            has_next_page = len(bank_rows) > limit
            if has_next_page:
                bank_rows = bank_rows[:limit]
            
            # Convert to GraphQL types
            edges = []
            for idx, row in enumerate(bank_rows):
                bank = BankType(
                    id=row['id'],
                    name=row['name']
                )
                cursor = base64.b64encode(str(offset + idx).encode()).decode()
                edges.append(BankEdge(node=bank, cursor=cursor))
            
            # Page info
            page_info = PageInfo(
                has_next_page=has_next_page,
                has_previous_page=offset > 0,
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None
            )
            
            logger.info(f"Returning {len(edges)} banks, total: {total_count}")
            return BankConnection(
                edges=edges,
                page_info=page_info,
                total_count=total_count
            )
        
        except Exception as e:
            log_error(e, "Error in get_all_banks service")
            raise
    
    def get_bank_by_id(self, bank_id: int) -> Optional[BankType]:
        """
        Get bank by ID
        
        Args:
            bank_id: Bank ID
        
        Returns:
            Bank or None
        """
        logger.info(f"Getting bank by ID: {bank_id}")
        try:
            row = self.repo.get_bank_by_id(bank_id)
            if row:
                return BankType(id=row['id'], name=row['name'])
            return None
        except Exception as e:
            log_error(e, f"Error getting bank by ID: {bank_id}")
            raise


class BranchService:
    """Service for branch-related business logic"""
    
    def __init__(self):
        self.branch_repo = get_branch_repo()
        self.bank_repo = get_bank_repo()
        logger.info("BranchService initialized")
    
    def get_all_branches(
        self,
        first: int = 20,
        after: Optional[str] = None,
        filter_input: Optional[BranchFilterInput] = None
    ) -> BranchConnection:
        """
        Get all branches with pagination and filtering
        
        Args:
            first: Number of records to return
            after: Cursor for pagination
            filter_input: Filters to apply
        
        Returns:
            BranchConnection with edges and page info
        """
        logger.info(f"Getting branches - first: {first}, after: {after}, filters: {filter_input}")
        
        try:
            # Decode cursor to get offset
            offset = 0
            if after:
                try:
                    offset = int(base64.b64decode(after).decode()) + 1
                except Exception as e:
                    log_error(e, "Invalid cursor")
                    offset = 0
            
            # Apply max page size limit
            limit = min(first, settings.MAX_PAGE_SIZE)
            
            # Get data from repository with filters
            if filter_input and any([
                filter_input.ifsc,
                filter_input.city,
                filter_input.district,
                filter_input.state,
                filter_input.bank_name,
                filter_input.branch_name
            ]):
                branch_rows, total_count = self.branch_repo.search_branches(
                    ifsc=filter_input.ifsc,
                    city=filter_input.city,
                    district=filter_input.district,
                    state=filter_input.state,
                    bank_name=filter_input.bank_name,
                    branch_name=filter_input.branch_name,
                    limit=limit + 1,
                    offset=offset
                )
            else:
                branch_rows = self.branch_repo.get_all_branches(limit=limit + 1, offset=offset)
                total_count = self.branch_repo.count_branches()
            
            # Check if there are more results
            has_next_page = len(branch_rows) > limit
            if has_next_page:
                branch_rows = branch_rows[:limit]
            
            # Convert to GraphQL types
            edges = []
            for idx, row in enumerate(branch_rows):
                bank = BankType(
                    id=row['bank_id'],
                    name=row['bank_name']
                )
                
                branch = BranchType(
                    ifsc=row['ifsc'],
                    branch=row['branch'],
                    address=row['address'],
                    city=row['city'],
                    district=row['district'],
                    state=row['state'],
                    bank=bank
                )
                
                cursor = base64.b64encode(str(offset + idx).encode()).decode()
                edges.append(BranchEdge(node=branch, cursor=cursor))
            
            # Page info
            page_info = PageInfo(
                has_next_page=has_next_page,
                has_previous_page=offset > 0,
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None
            )
            
            logger.info(f"Returning {len(edges)} branches, total: {total_count}")
            return BranchConnection(
                edges=edges,
                page_info=page_info,
                total_count=total_count
            )
        
        except Exception as e:
            log_error(e, "Error in get_all_branches service")
            raise
    
    def get_branch_by_ifsc(self, ifsc: str) -> Optional[BranchType]:
        """
        Get branch by IFSC code
        
        Args:
            ifsc: IFSC code
        
        Returns:
            Branch or None
        """
        logger.info(f"Getting branch by IFSC: {ifsc}")
        try:
            row = self.branch_repo.get_branch_by_ifsc(ifsc)
            if row:
                bank = BankType(
                    id=row['bank_id'],
                    name=row['bank_name']
                )
                
                return BranchType(
                    ifsc=row['ifsc'],
                    branch=row['branch'],
                    address=row['address'],
                    city=row['city'],
                    district=row['district'],
                    state=row['state'],
                    bank=bank
                )
            return None
        except Exception as e:
            log_error(e, f"Error getting branch by IFSC: {ifsc}")
            raise


# Global service instances
bank_service = BankService()
branch_service = BranchService()


def get_bank_service() -> BankService:
    """Get bank service instance"""
    return bank_service


def get_branch_service() -> BranchService:
    """Get branch service instance"""
    return branch_service

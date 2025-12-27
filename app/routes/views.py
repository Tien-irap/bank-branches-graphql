"""
GraphQL Views - The "Doorway"
Query definitions and resolvers for GraphQL endpoint
"""
from typing import Optional
import strawberry

from app.schemas import BranchConnection, BankConnection, BranchType, BankType, BranchFilterInput
from app.services import get_branch_service, get_bank_service
from app.core.logger import logger, log_graphql_query


@strawberry.type
class Query:
    """GraphQL Query Root"""
    
    @strawberry.field
    def branches(
        self,
        first: int = 20,
        after: Optional[str] = None,
        filter: Optional[BranchFilterInput] = None
    ) -> BranchConnection:
        """
        Query all branches with pagination and filtering
        
        Args:
            first: Number of branches to return (default: 20, max: 100)
            after: Cursor for pagination
            filter: Filter criteria
        
        Returns:
            BranchConnection with edges and page info
        
        Example:
            query {
                branches(first: 10) {
                    edges {
                        node {
                            ifsc
                            branch
                            city
                            bank {
                                name
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        endCursor
                    }
                    totalCount
                }
            }
        """
        log_graphql_query(
            "branches",
            {"first": first, "after": after, "filter": filter}
        )
        logger.info(f"GraphQL Query: branches(first={first}, after={after}, filter={filter})")
        
        service = get_branch_service()
        return service.get_all_branches(first=first, after=after, filter_input=filter)
    
    @strawberry.field
    def branch(self, ifsc: str) -> Optional[BranchType]:
        """
        Query a single branch by IFSC code
        
        Args:
            ifsc: IFSC code
        
        Returns:
            Branch or None
        
        Example:
            query {
                branch(ifsc: "ABHY0065001") {
                    ifsc
                    branch
                    address
                    city
                    bank {
                        name
                    }
                }
            }
        """
        log_graphql_query("branch", {"ifsc": ifsc})
        logger.info(f"GraphQL Query: branch(ifsc={ifsc})")
        
        service = get_branch_service()
        return service.get_branch_by_ifsc(ifsc)
    
    @strawberry.field
    def banks(
        self,
        first: int = 20,
        after: Optional[str] = None
    ) -> BankConnection:
        """
        Query all banks with pagination
        
        Args:
            first: Number of banks to return (default: 20, max: 100)
            after: Cursor for pagination
        
        Returns:
            BankConnection with edges and page info
        
        Example:
            query {
                banks(first: 10) {
                    edges {
                        node {
                            id
                            name
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    totalCount
                }
            }
        """
        log_graphql_query("banks", {"first": first, "after": after})
        logger.info(f"GraphQL Query: banks(first={first}, after={after})")
        
        service = get_bank_service()
        return service.get_all_banks(first=first, after=after)
    
    @strawberry.field
    def bank(self, id: int) -> Optional[BankType]:
        """
        Query a single bank by ID
        
        Args:
            id: Bank ID
        
        Returns:
            Bank or None
        
        Example:
            query {
                bank(id: 60) {
                    id
                    name
                }
            }
        """
        log_graphql_query("bank", {"id": id})
        logger.info(f"GraphQL Query: bank(id={id})")
        
        service = get_bank_service()
        return service.get_bank_by_id(id)


# Create the GraphQL schema
schema = strawberry.Schema(query=Query)

# gh_store/handlers/comment.py

import json
from typing import Sequence
from loguru import logger
from github import Repository, IssueComment
from omegaconf import DictConfig

from ..core.types import StoredObject, Update
from ..core.exceptions import InvalidUpdate
from ..core.access import AccessControl

class CommentHandler:
    """Handles processing of update comments"""
    
    def __init__(self, repo: Repository.Repository, config: DictConfig):
        self.repo = repo
        self.config = config
        self.processed_reaction = config.store.reactions.processed
        self.initial_state_reaction = config.store.reactions.initial_state
        self.access_control = AccessControl(repo)

    def get_unprocessed_updates(self, issue_number: int) -> list[Update]:
        """Get all unprocessed updates from issue comments"""
        logger.info(f"Fetching unprocessed updates for issue #{issue_number}")
        
        issue = self.repo.get_issue(issue_number)
        updates = []
        
        for comment in issue.get_comments():
            if self._is_processed(comment):
                continue
                
            try:
                update_data = json.loads(comment.body)
                
                # Skip initial state comments
                if isinstance(update_data, dict) and update_data.get("type") == "initial_state":
                    logger.debug(f"Skipping initial state comment {comment.id}")
                    continue
                    
                # Skip comments from unauthorized users
                if not self.access_control.validate_comment_author(comment):
                    logger.debug(f"Skipping unauthorized comment {comment.id}")
                    continue
                    
                # Parse and normalize JSON data
                if not isinstance(update_data, dict):
                    update_data = {"data": update_data}
                    
                updates.append(Update(
                    comment_id=comment.id,
                    timestamp=comment.created_at,
                    changes=update_data
                ))
            except json.JSONDecodeError:
                # Not JSON, skip it
                logger.debug(f"Skipping non-JSON comment {comment.id}")
                continue
        
        return sorted(updates, key=lambda u: u.timestamp)

    def apply_update(self, obj: StoredObject, update: Update) -> StoredObject:
        """Apply an update to an object"""
        logger.info(f"Applying update {update.comment_id} to {obj.meta.object_id}")
        
        # Deep merge the changes into the existing data
        updated_data = self._deep_merge(obj.data, update.changes)
        
        # Create new object with updated data and incremented version
        return StoredObject(
            meta=obj.meta,
            data=updated_data
        )

    def mark_processed(
        self, 
        issue_number: int,
        updates: Sequence[Update]
    ) -> None:
        """Mark comments as processed by adding reactions"""
        logger.info(f"Marking {len(updates)} comments as processed")
        
        issue = self.repo.get_issue(issue_number)
        
        for update in updates:
            for comment in issue.get_comments():
                if comment.id == update.comment_id:
                    comment.create_reaction(self.processed_reaction)
                    break

    def _is_processed(self, comment: IssueComment.IssueComment) -> bool:
        """Check if a comment has been processed"""
        for reaction in comment.get_reactions():
            if reaction.content == self.processed_reaction:
                return True
        return False

    def _deep_merge(self, base: dict, update: dict) -> dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result

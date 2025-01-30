from typing import Optional
import os.path as osp
import shutil
import subprocess
from subprocess import CompletedProcess
import filelock


def _get_stdout(p: CompletedProcess) -> str:
    return p.stdout.decode()


def _get_stderr(p: CompletedProcess) -> str:
    return p.stderr.decode()


def _run_git(*args: list[str], check=True) -> CompletedProcess:
    ret = subprocess.run(['git'] + list(args), check=check, capture_output=True)
    return ret


def get_repo_root():
    '''
    return: repo root path
    '''
    return _get_stdout(_run_git('rev-parse', '--show-toplevel')).strip()


def _get_repo():
    return osp.join(get_repo_root(), '.git')


def _get_repo_index_file() -> Optional[str]:
    file = osp.join(_get_repo(), 'index')
    if osp.exists(file):
        return file
    return None


def curr_commit_id() -> str:
    '''
    return: current git commit id
    '''
    return _get_stdout(
        _run_git('rev-parse', 'HEAD')
    ).strip()


def curr_branch_name() -> Optional[str]:
    '''
    return: current git branch name
    '''
    p = _run_git('symbolic-ref', '--short', 'HEAD', check=False)
    if p.returncode != 0:
        return None
    return _get_stdout(p).strip()


def is_valid_repo() -> bool:
    '''
    return: current repo is valid for gsnapshot
    '''
    try:
        curr_commit_id()
    except:
        return False
    return True

def _backup_index_file() -> Optional[str]:
    index_file = _get_repo_index_file()
    if index_file is None:
        return None
    backup_file = index_file + '.bak'
    shutil.copy2(index_file, backup_file)
    return backup_file


def _need_new_commit() -> bool:
    ret = _get_stdout(_run_git('status', '--short')).strip()
    return ret != ''


def _create_tag(tag_anno: str, tag_msg: str):
    _run_git('tag', '-a', tag_anno, '-m', tag_msg)


def _commit_all(commit_msg: str):
    # pre gc, avoid pre staged object lost
    _run_git('gc', '--auto')

    # clear stage
    _run_git('reset', 'head')

    # add all to stage
    _run_git('add', '-A', get_repo_root())

    # commit all with commit message
    _run_git('commit', '-m', commit_msg)


def snapshot_repo(tag_anno: str, tag_msg: str, commit_msg: str) -> str:
    '''
    tag_anno: str, tag name for new created tag
    tag_msg: str, tag message for new created tag message
    commit_msg: str, commit message for new created commit (if created)

    return: snapshot commit id
    '''

    if not is_valid_repo():
        raise ValueError('not a valid repo, not a git repo or no commit exist') 
    
    LOCK_FILE_NAME = '.gsnapshot_snapshot.lock'
    snapshot_lock_file = osp.join(_get_repo(), LOCK_FILE_NAME)
    start_commit_id = curr_commit_id()
    branch_name = curr_branch_name()

    lock = filelock.FileLock(snapshot_lock_file)
    with lock:
        # first backup index file
        backup_index_file = _backup_index_file()

        # check need new commit
        if _need_new_commit():
            _commit_all(commit_msg)
            _create_tag(tag_anno, tag_msg)
            ret = curr_commit_id()
            # rewind
            if branch_name is not None:
                # rewind branch 
                _run_git('update-ref', f'refs/heads/{branch_name}', start_commit_id)
            else:
                # rewind head
                _run_git('reset', '--soft', start_commit_id)
        else:
            # create tag
            _create_tag(tag_anno, tag_msg)
            ret = start_commit_id
        
        # recover index file
        if backup_index_file is not None:
            shutil.copy2(backup_index_file, _get_repo_index_file())
    return ret












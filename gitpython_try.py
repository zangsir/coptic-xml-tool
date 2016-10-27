from git import Repo
repo=Repo('/Users/zangsir/repo/MCtone-learning/')
git=repo.git
git.add('YI-XU-DATA/readme-data-qp2.txt')
git.commit('YI-XU-DATA/readme-data-qp2.txt','-m soem')
git.push()
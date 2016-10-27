from gittle import Gittle
repo_url='https://github.com/zangsir/MCtone-learning.git'
repo_path='/Users/zangsir/repo/MCtone-learning/'

g = Gittle(repo_path, origin_uri=repo_url)

#g.tracked_files
#g.modified_files

g.stage('YI-XU-DATA/readme-data-qp2.txt')

g.commit(name='Shuo Zhang',email='zangsir@gmail.com',message='minor change')
g.auth(username="zangsir@gmail.com", password="zs12084")
g.push(origin_uri="https://github.com/zangsir/MCtone-learning.git")